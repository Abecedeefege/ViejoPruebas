"""Pipeline de voz: WhatsApp (WebRTC) ↔ OpenAI Realtime (gpt-realtime-2.1).

Audio speech-to-speech directo: el transporte SmallWebRTC de Pipecat entrega el
audio Opus de WhatsApp como PCM, el servicio Realtime de OpenAI conversa, y la
salida vuelve por el mismo transceiver.
"""

from __future__ import annotations

import asyncio

from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.openai.realtime.events import (
    AudioConfiguration,
    AudioInput,
    AudioOutput,
    SemanticTurnDetection,
    SessionProperties,
)
from pipecat.services.openai.realtime.llm import OpenAIRealtimeLLMService
from pipecat.transports.base_transport import TransportParams
from pipecat.transports.smallwebrtc.transport import SmallWebRTCTransport

from .config import get_settings
from .prompts import SPARRING_INSTRUCTIONS
from .rtc import OutboundWhatsAppConnection, filter_sdp_for_whatsapp


class WhatsAppCallConnection(OutboundWhatsAppConnection):
    """Conexión WebRTC de una llamada WhatsApp (sirve para salientes y entrantes)."""

    async def create_answer_for(self, sdp: str, sdp_type: str) -> str:
        """Rol answerer (llamada entrante): genera el SDP answer filtrado para Meta."""
        await self.initialize(sdp=sdp, type=sdp_type)
        answer = self.get_answer()
        if not answer or not answer.get("sdp"):
            raise RuntimeError("SmallWebRTC no produjo SDP answer")
        return filter_sdp_for_whatsapp(answer["sdp"])


def make_connection() -> WhatsAppCallConnection:
    return WhatsAppCallConnection()


async def start_pipeline(connection, session) -> asyncio.Task:
    """Arma y lanza el pipeline para una llamada ya negociada.

    Devuelve el asyncio.Task del runner (handle con .cancel() para el manager).
    """
    settings = get_settings()

    transport = SmallWebRTCTransport(
        webrtc_connection=connection,
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        ),
    )

    session_properties = SessionProperties(
        instructions=SPARRING_INSTRUCTIONS,
        audio=AudioConfiguration(
            input=AudioInput(turn_detection=SemanticTurnDetection()),
            output=AudioOutput(voice=settings.openai_voice),
        ),
    )
    llm = OpenAIRealtimeLLMService(
        api_key=settings.openai_api_key,
        model=settings.openai_realtime_model,
        session_properties=session_properties,
    )

    pipeline = Pipeline([transport.input(), llm, transport.output()])
    task = PipelineTask(pipeline)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(_transport, _client):
        logger.info(f"[{session.ref}] audio conectado, arranca la conversación")
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(_transport, _client):
        logger.info(f"[{session.ref}] audio desconectado")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=False)
    return asyncio.create_task(runner.run(task), name=f"pipeline-{session.ref}")
