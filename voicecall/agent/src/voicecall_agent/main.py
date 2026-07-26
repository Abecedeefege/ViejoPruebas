"""API del agente: webhooks de Meta + API interna para la web."""

from __future__ import annotations

import asyncio
import json
import re
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel

from .call_manager import CallManager, ConnectionFactory, PipelineStarter
from .config import get_settings
from .events import parse_webhook
from .permissions import PermissionStore, normalize_wa_id
from .prompts import PERMISSION_REQUEST_TEXT
from .security import require_bearer, verify_meta_signature
from .whatsapp_calls import WhatsAppGraphClient

E164_RE = re.compile(r"^\+\d{8,15}$")


class CallRequest(BaseModel):
    to: str


def create_app(
    connection_factory: ConnectionFactory | None = None,
    pipeline_starter: PipelineStarter | None = None,
) -> FastAPI:
    """Crea la app. Los factories son inyectables para tests; por defecto usa el bot real."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings = get_settings()
        factory = connection_factory
        starter = pipeline_starter
        if factory is None or starter is None:
            from . import bot  # import tardío: aiortc/pipecat solo cuando corre en serio

            factory = factory or bot.make_connection
            starter = starter or bot.start_pipeline

        http = httpx.AsyncClient(timeout=30)
        graph = WhatsAppGraphClient(
            access_token=settings.whatsapp_access_token,
            phone_number_id=settings.whatsapp_phone_number_id,
            http=http,
            api_version=settings.graph_api_version,
        )
        app.state.manager = CallManager(
            graph=graph,
            permissions=PermissionStore(),
            connection_factory=factory,
            pipeline_starter=starter,
            permission_text=PERMISSION_REQUEST_TEXT,
            max_call_seconds=settings.max_call_minutes * 60,
        )
        logger.info("voicecall-agent listo")
        try:
            yield
        finally:
            await app.state.manager.shutdown()
            await http.aclose()

    app = FastAPI(title="voicecall-agent", lifespan=lifespan)

    # ── Webhooks de Meta ───────────────────────────────────────────────────

    @app.get("/webhooks/whatsapp")
    async def verify_webhook(request: Request):
        settings = get_settings()
        params = request.query_params
        if (
            params.get("hub.mode") == "subscribe"
            and params.get("hub.verify_token") == settings.whatsapp_verify_token
            and params.get("hub.challenge")
        ):
            return PlainTextResponse(params["hub.challenge"])
        raise HTTPException(status_code=403, detail="verificación inválida")

    @app.post("/webhooks/whatsapp")
    async def receive_webhook(request: Request):
        settings = get_settings()
        raw = await request.body()
        signature = request.headers.get("X-Hub-Signature-256")
        if not verify_meta_signature(raw, signature, settings.meta_app_secret):
            raise HTTPException(status_code=403, detail="firma inválida")
        try:
            payload = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="JSON inválido")

        events = parse_webhook(payload)
        # Responder rápido: Meta reintenta si tardamos; el SDP/ICE se procesa aparte.
        for event in events:
            asyncio.create_task(request.app.state.manager.handle_event(event))
        return {"received": len(events)}

    # ── API interna (la usa la web) ────────────────────────────────────────

    @app.post("/calls", dependencies=[Depends(require_bearer)])
    async def create_call(body: CallRequest, request: Request):
        settings = get_settings()
        to = "+" + normalize_wa_id(body.to)
        if not E164_RE.match(to):
            raise HTTPException(status_code=422, detail="número inválido (esperado E.164, ej +5491155550000)")
        allowed = {normalize_wa_id(n) for n in settings.allowed_list}
        if normalize_wa_id(to) not in allowed:
            raise HTTPException(
                status_code=403,
                detail="destino no permitido: agregalo a ALLOWED_DESTINATIONS",
            )
        session = await request.app.state.manager.request_call(to)
        return session.public()

    @app.get("/calls/{ref}", dependencies=[Depends(require_bearer)])
    async def get_call(ref: str, request: Request):
        session = request.app.state.manager.get(ref)
        if not session:
            raise HTTPException(status_code=404, detail="llamada no encontrada")
        return session.public()

    @app.get("/calls", dependencies=[Depends(require_bearer)])
    async def list_calls(request: Request):
        return request.app.state.manager.snapshot()

    @app.get("/healthz")
    async def healthz():
        return {"ok": True}

    return app


app = create_app()


def run() -> None:
    import uvicorn

    settings = get_settings()
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    run()
