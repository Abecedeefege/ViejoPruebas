"""Parseo de webhooks con payloads tomados de la doc oficial de la Calling API."""

from voicecall_agent.events import (
    CallConnect,
    CallStatus,
    CallTerminate,
    PermissionReply,
    parse_webhook,
)


def _entry(value: dict, field: str) -> dict:
    return {
        "object": "whatsapp_business_account",
        "entry": [{"id": "WABA_ID", "changes": [{"value": value, "field": field}]}],
    }


METADATA = {"display_phone_number": "16315553601", "phone_number_id": "111222333"}


def test_connect_saliente_con_answer():
    payload = _entry(
        {
            "messaging_product": "whatsapp",
            "metadata": METADATA,
            "calls": [
                {
                    "id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
                    "to": "16315553601",
                    "from": "16315553602",
                    "event": "connect",
                    "timestamp": "1671644824",
                    "direction": "BUSINESS_INITIATED",
                    "session": {"sdp_type": "answer", "sdp": "v=0\r\n..."},
                }
            ],
        },
        "calls",
    )
    events = parse_webhook(payload)
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CallConnect)
    assert event.call_id == "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh"
    assert event.direction == "BUSINESS_INITIATED"
    assert event.sdp_type == "answer"
    assert event.sdp.startswith("v=0")


def test_connect_entrante_con_offer():
    payload = _entry(
        {
            "messaging_product": "whatsapp",
            "metadata": METADATA,
            "contacts": [{"profile": {"name": "Andrés"}, "wa_id": "5491155550000"}],
            "calls": [
                {
                    "id": "wacid.ENTRANTE",
                    "to": "16315553601",
                    "from": "5491155550000",
                    "event": "connect",
                    "timestamp": "1671644824",
                    "direction": "USER_INITIATED",
                    "session": {"sdp_type": "offer", "sdp": "v=0\r\noffer"},
                }
            ],
        },
        "calls",
    )
    (event,) = parse_webhook(payload)
    assert isinstance(event, CallConnect)
    assert event.sdp_type == "offer"
    assert event.from_number == "5491155550000"


def test_status_ringing():
    payload = _entry(
        {
            "messaging_product": "whatsapp",
            "metadata": METADATA,
            "statuses": [
                {
                    "id": "wacid.ABGGFjFVU2AfAgo6V",
                    "timestamp": "1671644824",
                    "type": "call",
                    "status": "RINGING",
                    "recipient_id": "163155536021",
                    "biz_opaque_callback_data": "ref123",
                }
            ],
        },
        "calls",
    )
    (event,) = parse_webhook(payload)
    assert isinstance(event, CallStatus)
    assert event.status == "RINGING"
    assert event.call_id == "wacid.ABGGFjFVU2AfAgo6V"


def test_terminate():
    payload = _entry(
        {
            "messaging_product": "whatsapp",
            "metadata": METADATA,
            "calls": [
                {
                    "id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
                    "to": "16315553601",
                    "from": "16315553602",
                    "event": "terminate",
                    "direction": "BUSINESS_INITIATED",
                    "timestamp": "1671644824",
                    "status": "COMPLETED",
                    "start_time": "1671644824",
                    "end_time": "1671644944",
                    "duration": 120,
                }
            ],
        },
        "calls",
    )
    (event,) = parse_webhook(payload)
    assert isinstance(event, CallTerminate)
    assert event.status == "COMPLETED"
    assert event.duration == 120


def test_permission_reply_accept():
    payload = _entry(
        {
            "messaging_product": "whatsapp",
            "metadata": METADATA,
            "messages": [
                {
                    "from": "5491155550000",
                    "id": "wamid.XYZ",
                    "timestamp": "1671644824",
                    "type": "interactive",
                    "interactive": {
                        "type": "call_permission_reply",
                        "call_permission_reply": {
                            "response": "accept",
                            "is_permanent": False,
                            "expiration_timestamp": 1745343479,
                        },
                    },
                }
            ],
        },
        "messages",
    )
    (event,) = parse_webhook(payload)
    assert isinstance(event, PermissionReply)
    assert event.response == "accept"
    assert event.from_wa_id == "5491155550000"
    assert event.expiration_timestamp == 1745343479


def test_mensaje_de_texto_se_ignora():
    payload = _entry(
        {
            "messaging_product": "whatsapp",
            "metadata": METADATA,
            "messages": [
                {
                    "from": "5491155550000",
                    "id": "wamid.TXT",
                    "timestamp": "1671644824",
                    "type": "text",
                    "text": {"body": "hola"},
                }
            ],
        },
        "messages",
    )
    assert parse_webhook(payload) == []


def test_payload_vacio():
    assert parse_webhook({}) == []
