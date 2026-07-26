"""WebRTC para llamadas WhatsApp salientes.

Pipecat trae `SmallWebRTCConnection` pensada para el rol *answerer* (llamadas
entrantes: llega el offer de WhatsApp y generamos el answer). Para las llamadas
salientes el negocio tiene que mandar el OFFER en `POST /{PHONE_ID}/calls`, así
que acá extendemos la conexión para poder actuar como *offerer* usando el
RTCPeerConnection interno (aiortc) que la clase expone vía `.pc`.

El transporte de Pipecat (`SmallWebRTCTransport`) usa el transceiver 0 para
audio (entrada por evento `track-started`, salida por `replace_audio_track`),
por eso creamos un único transceiver de audio `sendrecv` antes del offer.
"""

from aiortc import RTCSessionDescription
from loguru import logger

from pipecat.transports.smallwebrtc.connection import IceServer, SmallWebRTCConnection

DEFAULT_ICE_SERVERS = [IceServer(urls="stun:stun.l.google.com:19302")]


def filter_sdp_for_whatsapp(sdp: str) -> str:
    """WhatsApp solo acepta fingerprints sha-256: filtramos el resto.

    (Mismo criterio que usa el cliente WhatsApp oficial de Pipecat para los
    answers de llamadas entrantes; Meta rechaza SDP con sha-384/sha-512.)
    """
    lines = sdp.splitlines()
    filtered = [
        line
        for line in lines
        if not (
            line.startswith("a=fingerprint:") and not line.startswith("a=fingerprint:sha-256")
        )
    ]
    return "\r\n".join(filtered) + "\r\n"


class OutboundWhatsAppConnection(SmallWebRTCConnection):
    """`SmallWebRTCConnection` con soporte de rol offerer para llamadas salientes."""

    def __init__(self, ice_servers: list[IceServer] | None = None, **kwargs):
        super().__init__(ice_servers or DEFAULT_ICE_SERVERS, **kwargs)

    async def create_offer(self) -> str:
        """Crea el SDP offer (con ICE candidates ya incluidos) para mandarle a Meta.

        aiortc completa el ICE gathering dentro de `setLocalDescription`, así que
        `localDescription.sdp` ya sale con los candidates (Meta no soporta trickle).
        """
        self.pc.addTransceiver("audio", direction="sendrecv")
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        sdp = self.pc.localDescription.sdp
        logger.debug(f"SDP offer generado ({len(sdp)} bytes) para {self.pc_id}")
        return filter_sdp_for_whatsapp(sdp)

    async def apply_remote_answer(self, sdp: str) -> None:
        """Aplica el SDP answer que llega por webhook cuando el usuario atiende."""
        logger.debug(f"Aplicando SDP answer remoto en {self.pc_id}")
        await self.pc.setRemoteDescription(RTCSessionDescription(sdp=sdp, type="answer"))
