"""Flujo completo del CallManager con fakes (sin red, sin WebRTC real)."""

import asyncio

import pytest

from voicecall_agent.call_manager import CallManager
from voicecall_agent.events import CallConnect, CallStatus, CallTerminate, PermissionReply
from voicecall_agent.permissions import PermissionStore
from voicecall_agent.whatsapp_calls import WhatsAppApiError

TO = "+5491155550000"
WA_ID = "5491155550000"


class FakeGraph:
    def __init__(self, permission_state=None, fail_first_initiate=False):
        self.permission_requests: list[str] = []
        self.initiated: list[tuple[str, str]] = []
        self.terminated: list[str] = []
        self.inbound_answers: list[tuple[str, str, str]] = []
        self.permission_state = permission_state
        self.fail_first_initiate = fail_first_initiate

    async def send_call_permission_request(self, to, text):
        self.permission_requests.append(to)
        return {"messages": [{"id": "wamid.PERM"}]}

    async def get_call_permission_state(self, wa_id):
        return self.permission_state

    async def initiate_call(self, to, sdp_offer, callback_data=None):
        if self.fail_first_initiate:
            self.fail_first_initiate = False
            raise WhatsAppApiError("(#138006) sin permiso", code=138006)
        self.initiated.append((to, sdp_offer))
        return f"wacid.TEST{len(self.initiated)}"

    async def terminate_call(self, call_id):
        self.terminated.append(call_id)
        return {"success": True}

    async def answer_inbound_call(self, call_id, to, sdp_answer):
        self.inbound_answers.append((call_id, to, sdp_answer))


class FakeConnection:
    def __init__(self):
        self.remote_answer = None
        self.disconnected = False

    async def create_offer(self):
        return "v=0 OFFER"

    async def create_answer_for(self, sdp, sdp_type):
        return "v=0 ANSWER"

    async def apply_remote_answer(self, sdp):
        self.remote_answer = sdp

    async def disconnect(self):
        self.disconnected = True


class FakePipeline:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True


def make_manager(graph=None, seeded_permission=False):
    graph = graph or FakeGraph()
    permissions = PermissionStore()
    if seeded_permission:
        permissions.on_reply(PermissionReply(from_wa_id=WA_ID, response="accept"))
    pipelines: list[FakePipeline] = []

    async def starter(connection, session):
        pipeline = FakePipeline()
        pipelines.append(pipeline)
        return pipeline

    manager = CallManager(
        graph=graph,
        permissions=permissions,
        connection_factory=FakeConnection,
        pipeline_starter=starter,
        permission_text="¿puedo llamarte?",
        max_call_seconds=600,
    )
    return manager, graph, pipelines


async def test_sin_permiso_pide_y_luego_llama():
    manager, graph, pipelines = make_manager()

    session = await manager.request_call(TO)
    assert session.state == "permission_requested"
    assert graph.permission_requests == [TO]
    assert graph.initiated == []

    # El usuario acepta el permiso desde WhatsApp → se inicia la llamada sola
    await manager.handle_event(PermissionReply(from_wa_id=WA_ID, response="accept"))
    assert session.state == "calling"
    assert len(graph.initiated) == 1
    assert graph.initiated[0][0] == TO
    call_id = session.call_id
    assert call_id == "wacid.TEST1"

    # Suena
    await manager.handle_event(CallStatus(call_id=call_id, status="RINGING"))
    assert session.state == "ringing"

    # Atiende: llega el SDP answer → arranca el pipeline
    await manager.handle_event(
        CallConnect(
            call_id=call_id,
            from_number="16315553601",
            to_number=WA_ID,
            direction="BUSINESS_INITIATED",
            sdp_type="answer",
            sdp="v=0 REMOTE-ANSWER",
        )
    )
    assert session.state == "in_call"
    assert session.connection.remote_answer == "v=0 REMOTE-ANSWER"
    assert len(pipelines) == 1

    # Cuelga
    connection = session.connection
    await manager.handle_event(CallTerminate(call_id=call_id, status="COMPLETED", duration=42))
    assert session.state == "ended"
    assert pipelines[0].cancelled
    assert connection.disconnected


async def test_con_permiso_vigente_llama_directo():
    manager, graph, _ = make_manager(seeded_permission=True)
    session = await manager.request_call(TO)
    assert session.state == "calling"
    assert graph.permission_requests == []
    assert len(graph.initiated) == 1


async def test_permiso_vigente_en_meta_pero_no_en_cache():
    graph = FakeGraph(
        permission_state={"permission": {"status": "temporary", "expiration_time": None}}
    )
    manager, graph, _ = make_manager(graph=graph)
    session = await manager.request_call(TO)
    assert session.state == "calling"
    assert graph.permission_requests == []


async def test_error_138006_cae_a_pedir_permiso():
    graph = FakeGraph(
        fail_first_initiate=True,
        permission_state={"permission": {"status": "temporary", "expiration_time": None}},
    )
    manager, graph, _ = make_manager(graph=graph)
    session = await manager.request_call(TO)
    # Meta decía temporary pero al llamar dio 138006 → pedimos permiso
    assert session.state == "permission_requested"
    assert graph.permission_requests == [TO]


async def test_permiso_rechazado():
    manager, graph, _ = make_manager()
    session = await manager.request_call(TO)
    await manager.handle_event(PermissionReply(from_wa_id=WA_ID, response="reject"))
    assert session.state == "permission_denied"
    assert graph.initiated == []


async def test_llamada_rechazada():
    manager, graph, _ = make_manager(seeded_permission=True)
    session = await manager.request_call(TO)
    await manager.handle_event(
        CallTerminate(call_id=session.call_id, status="REJECTED")
    )
    assert session.state == "rejected"


async def test_entrante_se_atiende_con_bot():
    manager, graph, pipelines = make_manager()
    await manager.handle_event(
        CallConnect(
            call_id="wacid.IN",
            from_number="5491155550000",
            to_number="16315553601",
            direction="USER_INITIATED",
            sdp_type="offer",
            sdp="v=0 REMOTE-OFFER",
        )
    )
    assert graph.inbound_answers == [("wacid.IN", "5491155550000", "v=0 ANSWER")]
    assert len(pipelines) == 1
    sessions = manager.snapshot()
    assert sessions[0]["direction"] == "inbound"
    assert sessions[0]["state"] == "in_call"


async def test_watchdog_corta_por_duracion():
    manager, graph, _ = make_manager(seeded_permission=True)
    manager._max_call_seconds = 0.05
    session = await manager.request_call(TO)
    await manager.handle_event(
        CallConnect(
            call_id=session.call_id,
            from_number="x",
            to_number=WA_ID,
            direction="BUSINESS_INITIATED",
            sdp_type="answer",
            sdp="v=0",
        )
    )
    assert session.state == "in_call"
    await asyncio.sleep(0.15)
    assert graph.terminated == [session.call_id]
