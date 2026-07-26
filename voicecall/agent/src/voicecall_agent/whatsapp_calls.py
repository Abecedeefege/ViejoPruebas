"""Cliente de la Graph API de Meta para la WhatsApp Business Calling API.

Cubre lo que Pipecat no trae: llamadas salientes (business-initiated),
solicitudes de permiso de llamada y consulta del estado del permiso.
También expone el flujo de aceptación de llamadas entrantes (pre_accept +
accept) para no depender de dos clientes HTTP distintos.

Payloads según la doc oficial de la Calling API (Cloud API).
"""

from __future__ import annotations

from typing import Any

import httpx
from loguru import logger

# Código de error de Graph API cuando no hay permiso de llamada vigente.
PERMISSION_MISSING_ERROR_CODE = 138006


class WhatsAppApiError(Exception):
    """Error devuelto por la Graph API, con código y respuesta completa."""

    def __init__(self, message: str, code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.code = code
        self.response = response or {}

    @property
    def is_missing_permission(self) -> bool:
        return self.code == PERMISSION_MISSING_ERROR_CODE


class WhatsAppGraphClient:
    def __init__(
        self,
        access_token: str,
        phone_number_id: str,
        http: httpx.AsyncClient,
        api_version: str = "v23.0",
        base_url: str = "https://graph.facebook.com",
    ) -> None:
        self._token = access_token
        self._phone_number_id = phone_number_id
        self._http = http
        self._base = f"{base_url}/{api_version}/{phone_number_id}"

    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        resp = await self._http.post(f"{self._base}/{path}", json=payload, headers=self._headers)
        data = self._json(resp)
        if resp.status_code >= 400 or "error" in data:
            error = data.get("error", {})
            raise WhatsAppApiError(
                f"Graph API {path} falló ({resp.status_code}): {error.get('message', data)}",
                code=error.get("code"),
                response=data,
            )
        return data

    @staticmethod
    def _json(resp: httpx.Response) -> dict[str, Any]:
        try:
            return resp.json()
        except Exception:
            return {"raw": resp.text}

    # ── Permisos de llamada ────────────────────────────────────────────────

    async def send_call_permission_request(self, to: str, body_text: str) -> dict[str, Any]:
        """Manda el mensaje interactivo de pedido de permiso de llamada.

        Límite de Meta: 1 pedido por 24h y 2 por 7 días (se resetea al conectar
        una llamada). El usuario responde desde WhatsApp y llega un webhook
        `messages` con `interactive.call_permission_reply`.
        """
        logger.info(f"Enviando call permission request a {to}")
        return await self._post(
            "messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "interactive",
                "interactive": {
                    "type": "call_permission_request",
                    "action": {"name": "call_permission_request"},
                    "body": {"text": body_text},
                },
            },
        )

    async def get_call_permission_state(self, user_wa_id: str) -> dict[str, Any] | None:
        """Consulta el estado del permiso (GET /{PHONE_ID}/call_permissions).

        Devuelve el JSON de Meta o None si el endpoint falla (best-effort: el
        estado real igual se aprende de los webhooks y del error 138006).
        """
        try:
            resp = await self._http.get(
                f"{self._base}/call_permissions",
                params={"user_wa_id": user_wa_id.lstrip("+")},
                headers=self._headers,
            )
            data = self._json(resp)
            if resp.status_code >= 400 or "error" in data:
                logger.warning(f"call_permissions devolvió error para {user_wa_id}: {data}")
                return None
            return data
        except httpx.HTTPError as e:
            logger.warning(f"No se pudo consultar call_permissions: {e}")
            return None

    # ── Llamadas salientes (business-initiated) ────────────────────────────

    async def initiate_call(
        self, to: str, sdp_offer: str, callback_data: str | None = None
    ) -> str:
        """Inicia una llamada saliente con nuestro SDP offer. Devuelve el call_id (wacid...).

        Si no hay permiso vigente, Graph responde error 138006 →
        `WhatsAppApiError.is_missing_permission`.
        """
        payload: dict[str, Any] = {
            "messaging_product": "whatsapp",
            "to": to,
            "action": "connect",
            "session": {"sdp_type": "offer", "sdp": sdp_offer},
        }
        if callback_data:
            payload["biz_opaque_callback_data"] = callback_data
        data = await self._post("calls", payload)
        calls = data.get("calls") or []
        if not calls or "id" not in calls[0]:
            raise WhatsAppApiError(f"Respuesta sin call id: {data}", response=data)
        call_id = calls[0]["id"]
        logger.info(f"Llamada saliente iniciada a {to}: {call_id}")
        return call_id

    async def terminate_call(self, call_id: str) -> dict[str, Any]:
        return await self._post(
            "calls",
            {"messaging_product": "whatsapp", "call_id": call_id, "action": "terminate"},
        )

    # ── Llamadas entrantes (user-initiated) ────────────────────────────────

    async def answer_inbound_call(self, call_id: str, to: str, sdp_answer: str) -> None:
        """Acepta una llamada entrante: pre_accept y después accept (flujo requerido por Meta).

        El SDP answer tiene que ser idéntico en ambos pasos, si no Meta corta con
        "SDP answer does not match".
        """
        for action in ("pre_accept", "accept"):
            await self._post(
                "calls",
                {
                    "messaging_product": "whatsapp",
                    "call_id": call_id,
                    "to": to,
                    "action": action,
                    "session": {"sdp_type": "answer", "sdp": sdp_answer},
                },
            )
        logger.info(f"Llamada entrante {call_id} aceptada")

    async def reject_call(self, call_id: str) -> dict[str, Any]:
        return await self._post(
            "calls",
            {"messaging_product": "whatsapp", "call_id": call_id, "action": "reject"},
        )

    # ── Mensajes ───────────────────────────────────────────────────────────

    async def send_text(self, to: str, body: str) -> dict[str, Any]:
        """Mensaje de texto simple (avisos tipo "no pude llamarte")."""
        return await self._post(
            "messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "text",
                "text": {"body": body},
            },
        )
