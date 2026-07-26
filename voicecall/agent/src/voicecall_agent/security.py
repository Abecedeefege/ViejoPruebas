"""Validación de firma de webhooks de Meta y auth de la API interna."""

import hashlib
import hmac

from fastapi import Header, HTTPException

from .config import get_settings


def verify_meta_signature(raw_body: bytes, signature_header: str | None, app_secret: str) -> bool:
    """Valida X-Hub-Signature-256 ("sha256=<hex>") con HMAC-SHA256 del body crudo.

    Si no hay app_secret configurado se acepta todo (modo dev) — en producción
    META_APP_SECRET tiene que estar seteado.
    """
    if not app_secret:
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature_header.removeprefix("sha256="), expected)


async def require_bearer(authorization: str | None = Header(default=None)) -> None:
    """Dependencia FastAPI: exige `Authorization: Bearer <AGENT_API_TOKEN>`."""
    settings = get_settings()
    expected = f"Bearer {settings.agent_api_token}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="token inválido")
