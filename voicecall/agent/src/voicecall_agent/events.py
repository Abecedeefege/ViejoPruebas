"""Parseo de webhooks de WhatsApp Cloud API (campos `calls` y `messages`).

Formas de payload según la doc oficial de la Calling API:
- value.calls[]    → eventos de llamada: connect (con SDP), terminate
- value.statuses[] → estados: RINGING / ACCEPTED / REJECTED (type == "call")
- value.messages[] → respuestas interactivas, incluida call_permission_reply
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CallConnect:
    """El otro extremo aceptó: llega la sesión SDP (answer si la llamada la iniciamos nosotros,
    offer si es una llamada entrante del usuario)."""

    call_id: str
    from_number: str
    to_number: str
    direction: str  # BUSINESS_INITIATED | USER_INITIATED
    sdp_type: str  # offer | answer
    sdp: str


@dataclass
class CallStatus:
    call_id: str
    status: str  # RINGING | ACCEPTED | REJECTED
    recipient_id: str | None = None


@dataclass
class CallTerminate:
    call_id: str
    status: str | None = None  # COMPLETED | FAILED | ...
    duration: int | None = None


@dataclass
class PermissionReply:
    from_wa_id: str
    response: str  # accept | reject
    is_permanent: bool = False
    expiration_timestamp: int | None = None


Event = CallConnect | CallStatus | CallTerminate | PermissionReply


def parse_webhook(payload: dict[str, Any]) -> list[Event]:
    """Convierte un POST de webhook de Meta en una lista de eventos tipados.

    Ignora silenciosamente todo lo que no reconoce (mensajes de texto, reads, etc.).
    """
    events: list[Event] = []
    for entry in payload.get("entry", []) or []:
        for change in entry.get("changes", []) or []:
            value = change.get("value", {}) or {}
            events.extend(_parse_calls(value.get("calls") or []))
            events.extend(_parse_statuses(value.get("statuses") or []))
            events.extend(_parse_messages(value.get("messages") or []))
    return events


def _parse_calls(calls: list[dict[str, Any]]) -> list[Event]:
    events: list[Event] = []
    for call in calls:
        event = call.get("event")
        if event == "connect":
            session = call.get("session", {}) or {}
            events.append(
                CallConnect(
                    call_id=call.get("id", ""),
                    from_number=call.get("from", ""),
                    to_number=call.get("to", ""),
                    direction=call.get("direction", ""),
                    sdp_type=session.get("sdp_type", ""),
                    sdp=session.get("sdp", ""),
                )
            )
        elif event == "terminate":
            events.append(
                CallTerminate(
                    call_id=call.get("id", ""),
                    status=call.get("status"),
                    duration=call.get("duration"),
                )
            )
    return events


def _parse_statuses(statuses: list[dict[str, Any]]) -> list[Event]:
    return [
        CallStatus(
            call_id=s.get("id", ""),
            status=(s.get("status") or "").upper(),
            recipient_id=s.get("recipient_id"),
        )
        for s in statuses
        if s.get("type") == "call"
    ]


def _parse_messages(messages: list[dict[str, Any]]) -> list[Event]:
    events: list[Event] = []
    for msg in messages:
        interactive = msg.get("interactive") or {}
        if interactive.get("type") != "call_permission_reply":
            continue
        reply = interactive.get("call_permission_reply") or {}
        events.append(
            PermissionReply(
                from_wa_id=msg.get("from", ""),
                response=(reply.get("response") or "").lower(),
                is_permanent=bool(reply.get("is_permanent", False)),
                expiration_timestamp=reply.get("expiration_timestamp"),
            )
        )
    return events
