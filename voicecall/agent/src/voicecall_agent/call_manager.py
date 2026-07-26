"""Orquestación de llamadas: estados, permisos y ciclo de vida.

Independiente de Pipecat/aiortc: recibe una `connection_factory` y un
`pipeline_starter` inyectados (duck typing), así se testea con fakes.

Estados de una llamada saliente:
    queued → permission_requested → calling → ringing → in_call → ended
                       ↓                                    ↑
              permission_denied            (webhook connect con SDP answer)
Fallas en cualquier punto → failed / rejected / no_answer.
"""

from __future__ import annotations

import asyncio
import secrets
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from loguru import logger

from .events import CallConnect, CallStatus, CallTerminate, Event, PermissionReply
from .permissions import PermissionStore, normalize_wa_id
from .whatsapp_calls import WhatsAppApiError, WhatsAppGraphClient

ConnectionFactory = Callable[[], Any]
# (connection, session) -> handle con .cancel()
PipelineStarter = Callable[[Any, "CallSession"], Awaitable[Any]]


@dataclass
class CallSession:
    ref: str
    to: str  # E.164 con +
    wa_id: str  # sin +
    direction: str = "outbound"
    state: str = "queued"
    call_id: str | None = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    connection: Any = None
    pipeline: Any = None
    watchdog: asyncio.Task | None = None

    def public(self) -> dict[str, Any]:
        return {
            "ref": self.ref,
            "to": self.to,
            "direction": self.direction,
            "state": self.state,
            "call_id": self.call_id,
            "error": self.error,
            "created_at": self.created_at,
        }


class CallManager:
    def __init__(
        self,
        graph: WhatsAppGraphClient,
        permissions: PermissionStore,
        connection_factory: ConnectionFactory,
        pipeline_starter: PipelineStarter,
        permission_text: str,
        max_call_seconds: int = 600,
    ) -> None:
        self._graph = graph
        self._permissions = permissions
        self._connection_factory = connection_factory
        self._pipeline_starter = pipeline_starter
        self._permission_text = permission_text
        self._max_call_seconds = max_call_seconds
        self._sessions: dict[str, CallSession] = {}
        self._by_call_id: dict[str, CallSession] = {}
        self._pending_by_wa_id: dict[str, CallSession] = {}

    # ── API pública ────────────────────────────────────────────────────────

    def get(self, ref: str) -> CallSession | None:
        return self._sessions.get(ref)

    def snapshot(self) -> list[dict[str, Any]]:
        return [s.public() for s in sorted(self._sessions.values(), key=lambda s: -s.created_at)]

    async def request_call(self, to: str) -> CallSession:
        """Punto de entrada desde la web: pide que el agente llame a `to`."""
        session = CallSession(
            ref=secrets.token_urlsafe(8), to=to, wa_id=normalize_wa_id(to)
        )
        self._sessions[session.ref] = session

        if self._permissions.is_granted(to):
            await self._initiate(session)
            return session

        # Best-effort: puede haber permiso vigente que no vimos (reinicio, etc.)
        state = await self._graph.get_call_permission_state(session.wa_id)
        permission = (state or {}).get("permission") or {}
        if permission.get("status") in ("temporary", "permanent"):
            self._permissions.grant_from_api(
                session.wa_id, permission["status"], permission.get("expiration_time")
            )
            await self._initiate(session)
        else:
            await self._request_permission(session)
        return session

    async def handle_event(self, event: Event) -> None:
        """Procesa un evento parseado del webhook de Meta."""
        try:
            if isinstance(event, PermissionReply):
                await self._on_permission_reply(event)
            elif isinstance(event, CallStatus):
                self._on_status(event)
            elif isinstance(event, CallConnect):
                await self._on_connect(event)
            elif isinstance(event, CallTerminate):
                await self._on_terminate(event)
        except Exception as e:  # el webhook nunca debe romperse por un evento
            logger.exception(f"Error manejando evento {event}: {e}")

    async def shutdown(self) -> None:
        for session in list(self._sessions.values()):
            if session.state in ("calling", "ringing", "in_call") and session.call_id:
                try:
                    await self._graph.terminate_call(session.call_id)
                except Exception:
                    pass
            await self._cleanup(session, final_state="ended")

    # ── Flujo saliente ─────────────────────────────────────────────────────

    async def _request_permission(self, session: CallSession) -> None:
        try:
            await self._graph.send_call_permission_request(session.to, self._permission_text)
            session.state = "permission_requested"
            self._pending_by_wa_id[session.wa_id] = session
            logger.info(f"[{session.ref}] permiso solicitado a {session.to}")
        except WhatsAppApiError as e:
            session.state = "failed"
            session.error = f"No se pudo pedir permiso: {e}"
            logger.error(session.error)

    async def _initiate(self, session: CallSession) -> None:
        try:
            connection = self._connection_factory()
            session.connection = connection
            offer = await connection.create_offer()
            session.state = "calling"
            session.call_id = await self._graph.initiate_call(
                session.to, offer, callback_data=session.ref
            )
            self._by_call_id[session.call_id] = session
            logger.info(f"[{session.ref}] llamando a {session.to} ({session.call_id})")
        except WhatsAppApiError as e:
            await self._close_connection(session)
            if e.is_missing_permission:
                logger.info(f"[{session.ref}] sin permiso vigente (138006), lo pido")
                await self._request_permission(session)
            else:
                session.state = "failed"
                session.error = str(e)
                logger.error(f"[{session.ref}] {e}")
        except Exception as e:
            await self._close_connection(session)
            session.state = "failed"
            session.error = str(e)
            logger.exception(f"[{session.ref}] error iniciando llamada")

    async def _on_permission_reply(self, reply: PermissionReply) -> None:
        state = self._permissions.on_reply(reply)
        pending = self._pending_by_wa_id.pop(normalize_wa_id(reply.from_wa_id), None)
        logger.info(f"Permiso de {reply.from_wa_id}: {reply.response}")
        if not pending:
            return
        if state.granted:
            await self._initiate(pending)
        else:
            pending.state = "permission_denied"

    def _on_status(self, status: CallStatus) -> None:
        session = self._by_call_id.get(status.call_id)
        if not session:
            return
        if status.status == "RINGING":
            session.state = "ringing"
        elif status.status == "ACCEPTED":
            # el connect con SDP answer llega aparte; estado intermedio
            if session.state in ("calling", "ringing"):
                session.state = "accepted"
        elif status.status == "REJECTED":
            session.state = "rejected"
            asyncio.create_task(self._close_connection(session))

    async def _on_connect(self, event: CallConnect) -> None:
        if event.sdp_type == "answer":
            await self._on_outbound_answered(event)
        else:
            await self._on_inbound_call(event)

    async def _on_outbound_answered(self, event: CallConnect) -> None:
        session = self._by_call_id.get(event.call_id)
        if not session or not session.connection:
            logger.warning(f"Answer para llamada desconocida {event.call_id}")
            return
        await session.connection.apply_remote_answer(event.sdp)
        session.pipeline = await self._pipeline_starter(session.connection, session)
        session.state = "in_call"
        session.watchdog = asyncio.create_task(self._watchdog(session))
        logger.info(f"[{session.ref}] en llamada")

    async def _on_inbound_call(self, event: CallConnect) -> None:
        """Llamada entrante (user-initiated): el usuario nos llama y atendemos con el bot."""
        session = CallSession(
            ref=secrets.token_urlsafe(8),
            to=f"+{normalize_wa_id(event.from_number)}",
            wa_id=normalize_wa_id(event.from_number),
            direction="inbound",
            call_id=event.call_id,
        )
        self._sessions[session.ref] = session
        self._by_call_id[event.call_id] = session
        try:
            connection = self._connection_factory()
            session.connection = connection
            sdp_answer = await connection.create_answer_for(event.sdp, event.sdp_type)
            await self._graph.answer_inbound_call(event.call_id, event.from_number, sdp_answer)
            session.pipeline = await self._pipeline_starter(connection, session)
            session.state = "in_call"
            session.watchdog = asyncio.create_task(self._watchdog(session))
            logger.info(f"[{session.ref}] llamada entrante de {event.from_number} atendida")
        except Exception as e:
            session.state = "failed"
            session.error = str(e)
            logger.exception(f"[{session.ref}] error atendiendo llamada entrante")
            await self._close_connection(session)

    async def _on_terminate(self, event: CallTerminate) -> None:
        session = self._by_call_id.pop(event.call_id, None)
        if not session:
            return
        final = "ended"
        if event.status == "REJECTED":
            final = "rejected"
        elif event.status == "FAILED":
            final = "no_answer" if session.state in ("calling", "ringing") else "failed"
        await self._cleanup(session, final_state=final)
        logger.info(f"[{session.ref}] terminada ({final}, {event.duration or 0}s)")

    # ── Utilidades ─────────────────────────────────────────────────────────

    async def _watchdog(self, session: CallSession) -> None:
        await asyncio.sleep(self._max_call_seconds)
        if session.state == "in_call" and session.call_id:
            logger.warning(f"[{session.ref}] corte por límite de duración")
            try:
                await self._graph.terminate_call(session.call_id)
            except Exception as e:
                logger.error(f"[{session.ref}] error terminando por watchdog: {e}")

    async def _cleanup(self, session: CallSession, final_state: str) -> None:
        if session.watchdog and not session.watchdog.done():
            session.watchdog.cancel()
        if session.pipeline is not None:
            try:
                session.pipeline.cancel()
            except Exception:
                pass
            session.pipeline = None
        await self._close_connection(session)
        session.state = final_state

    async def _close_connection(self, session: CallSession) -> None:
        if session.connection is not None:
            try:
                await session.connection.disconnect()
            except Exception:
                pass
            session.connection = None
