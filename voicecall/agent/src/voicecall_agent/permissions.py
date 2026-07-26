"""Registro en memoria de permisos de llamada por usuario.

La fuente de verdad es Meta (webhook `call_permission_reply` + error 138006 al
llamar + endpoint `call_permissions`); esto es un cache local para decidir si
hace falta pedir permiso antes de intentar la llamada. Permisos temporales
duran 7 días (168 h) salvo que Meta mande `expiration_timestamp`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from .events import PermissionReply

TEMPORARY_PERMISSION_SECONDS = 7 * 24 * 3600


def normalize_wa_id(number: str) -> str:
    """Meta usa wa_ids sin '+' (ej: 5491155550000)."""
    return number.strip().lstrip("+").replace(" ", "").replace("-", "")


@dataclass
class PermissionState:
    granted: bool
    is_permanent: bool = False
    expires_at: float | None = None  # epoch seconds; None si es permanente

    def is_active(self, now: float | None = None) -> bool:
        if not self.granted:
            return False
        if self.is_permanent or self.expires_at is None:
            return self.granted
        return (now if now is not None else time.time()) < self.expires_at


class PermissionStore:
    def __init__(self) -> None:
        self._by_user: dict[str, PermissionState] = {}

    def on_reply(self, reply: PermissionReply, now: float | None = None) -> PermissionState:
        wa_id = normalize_wa_id(reply.from_wa_id)
        now = now if now is not None else time.time()
        if reply.response == "accept":
            expires_at: float | None
            if reply.is_permanent:
                expires_at = None
            elif reply.expiration_timestamp:
                expires_at = float(reply.expiration_timestamp)
            else:
                expires_at = now + TEMPORARY_PERMISSION_SECONDS
            state = PermissionState(
                granted=True, is_permanent=reply.is_permanent, expires_at=expires_at
            )
        else:
            state = PermissionState(granted=False)
        self._by_user[wa_id] = state
        return state

    def grant_from_api(self, wa_id: str, status: str, expiration_time: float | None) -> None:
        """Sincroniza desde GET /call_permissions (status: temporary|permanent|no_permission)."""
        wa_id = normalize_wa_id(wa_id)
        if status in ("temporary", "permanent"):
            self._by_user[wa_id] = PermissionState(
                granted=True,
                is_permanent=(status == "permanent"),
                expires_at=expiration_time,
            )
        else:
            self._by_user[wa_id] = PermissionState(granted=False)

    def revoke(self, wa_id: str) -> None:
        self._by_user[normalize_wa_id(wa_id)] = PermissionState(granted=False)

    def is_granted(self, wa_id: str, now: float | None = None) -> bool:
        state = self._by_user.get(normalize_wa_id(wa_id))
        return bool(state and state.is_active(now))
