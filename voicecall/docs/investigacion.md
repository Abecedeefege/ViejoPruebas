# Investigación: llamadas de voz por WhatsApp con IA (julio 2026)

Respuestas a: ¿cuál es la mejor manera de implementar "la web me llama por WhatsApp con
un agente de voz"? ¿Qué proveedores existen para agentes de ventas autónomos?

---

## 1. El "Talk API" nuevo de OpenAI

Lo que OpenAI anunció recientemente es **GPT‑Realtime‑2** (mayo 2026): su modelo
speech‑to‑speech con razonamiento clase GPT‑5, sucesor de `gpt-realtime` (GA desde
agosto 2025). En la API aparece como `gpt-realtime-2.1`. Vino acompañado de
`gpt-realtime-translate` (~$0.034/min) y `gpt-realtime-whisper` (~$0.017/min).

- **Transportes:** WebRTC (browser), **WebSocket** (server, el que usamos acá) y **SIP**
  (`sip:$PROJECT_ID@sip.api.openai.com;transport=tls`) para telefonía. El conector SIP
  solo recibe llamadas entrantes (webhook `realtime.call.incoming` → `POST /v1/realtime/calls/{id}/accept`).
- **Precio gpt‑realtime‑2:** $32 / 1M tokens de audio de entrada ($0.40 cacheado) y
  $64 / 1M de salida ≈ **USD 0,2–0,5 por minuto** de conversación real.

Fuentes: [anuncio gpt-realtime](https://openai.com/index/introducing-gpt-realtime/),
[anuncio modelos de voz 2026](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/),
[guía Realtime SIP](https://developers.openai.com/api/docs/guides/realtime-sip).

## 2. La única puerta a llamadas de voz por WhatsApp: la Calling API de Meta

La **WhatsApp Business Calling API** (Cloud API) es la vía oficial y única para hacer/recibir
llamadas VoIP de WhatsApp programáticamente. Datos clave verificados:

- **Media:** WebRTC con intercambio de SDP por Graph API + webhooks (`POST /{PHONE_ID}/calls`
  con offer; el answer llega por webhook `calls`). Codec **Opus** (también PCMA/PCMU).
  Alternativa: SIP (TLS + ICE/DTLS o SDES-SRTP). Solo acepta fingerprints **sha-256**.
- **Salientes (business-initiated):** requieren **permiso del usuario** (mensaje interactivo
  `call_permission_request`). Aceptado → dura **7 días** (o permanente si el usuario elige),
  hasta **5 llamadas/24 h** por usuario, máx. 1 pedido/24 h y 2/semana. Error `138006` = sin permiso.
- **Requisito de producción:** el número necesita **límite de mensajería ≥2.000
  destinatarios únicos/día** → implica **verificación de negocio de Meta** (1–2 semanas).
  **Los números de prueba/sandbox están EXENTOS** → ideal para el MVP personal.
- **Países:** salientes bloqueadas hacia EE.UU., Canadá, Egipto, Nigeria, Turquía, Vietnam.
  **Argentina OK** (Meta factura en ARS desde abr-2026). Entrantes: todo el mundo salvo sancionados.
- **Precios:** entrantes **gratis**; salientes por rate card del país en **pulsos de 6 segundos**,
  con descuentos por volumen.

Fuentes: [doc Calling API](https://developers.facebook.com/docs/whatsapp/cloud-api/calling/),
[pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing),
[integración WebRTC (webrtc.ventures)](https://webrtc.ventures/2025/11/how-to-integrate-the-whatsapp-business-calling-api-with-webrtc-to-enable-customer-voice-calls/).

## 3. Los tres caminos de implementación (y por qué elegimos el 1)

### Camino 1 — Meta directo + Pipecat (el que implementa este repo) ✅

Backend Python con [Pipecat](https://github.com/pipecat-ai/pipecat): transporte
SmallWebRTC (aiortc) contra WhatsApp + servicio `OpenAIRealtimeLLMService`
(speech‑to‑speech real con gpt‑realtime‑2.1).

- ✅ Arranca HOY con el número de prueba (sin verificación de negocio, sin costo de plataforma).
- ✅ Sin costo por minuto de intermediarios: pagás solo OpenAI + rate card de Meta.
- ✅ Control total (prompt, modelo, herramientas, datos).
- ⚠️ Pipecat trae de fábrica solo llamadas **entrantes** de WhatsApp; las **salientes**
  las implementamos nosotros (offer SDP propio + `POST /calls` + webhook answer — está en `agent/`).

### Camino 2 — Twilio managed (el camino natural a producción)

**WhatsApp Business Calling es GA en Twilio Programmable Voice desde el 15-jul-2025**:
llamadas salientes con la REST API (`whatsapp:{número}`) o TwiML
`<Dial callerId="whatsapp:+..."><WhatsApp>+54...</WhatsApp></Dial>`, e IA por
**Media Streams** (tutorial oficial Twilio+OpenAI Realtime, g711_ulaw) o **ConversationRelay**.

- ✅ Mucho menos código de media; infraestructura y reintentos resueltos.
- ❌ Exige WABA **verificada** con tier ≥2K (no sirve para el sandbox de hoy) y suma costo por minuto.
- Fuentes: [anuncio GA](https://www.twilio.com/en-us/blog/products/launches/generally-available-whatsapp-business-calling-twilio-voice),
  [docs](https://www.twilio.com/docs/voice/whatsapp-business-calling),
  [TwiML `<WhatsApp>`](https://www.twilio.com/docs/voice/twiml/whatsapp),
  [Twilio + OpenAI Realtime](https://www.twilio.com/en-us/blog/twilio-openai-realtime-api-launch-integration).

### Camino 3 — Plataforma llave en mano

**ElevenLabs Agents** soporta WhatsApp nativo (importás la WABA en su dashboard) con
llamadas **entrantes y salientes por API/UI**. Cero código de voz.

- ✅ Lo más rápido para un producto comercial sin equipo técnico.
- ❌ No usa gpt‑realtime (pipeline STT→LLM→TTS propio de ElevenLabs), lock‑in, igual necesitás WABA.
- Fuentes: [anuncio](https://elevenlabs.io/blog/elevenlabs-agents-whatsapp-support),
  [docs](https://elevenlabs.io/docs/eleven-agents/whatsapp).

**Estrategia recomendada:** MVP con Camino 1 (este repo) → si el producto crece,
verificación de negocio y evaluar quedarse en Meta directo (más barato) o migrar el
transporte a Twilio (menos operación), manteniendo el mismo pipeline de OpenAI.

## 4. Proveedores para agentes de ventas autónomos por voz

### Con llamadas de WhatsApp nativas

| Proveedor | Qué ofrece | Notas |
|---|---|---|
| [ElevenLabs Agents](https://elevenlabs.io/docs/eleven-agents/whatsapp) | Agente omnicanal (voz+chat) con WhatsApp in/out por API | El más completo hoy para WhatsApp voice llave en mano |
| [AiSensy AI Voice Calling](https://aisensy.com/features/voice-calling-ai) | Llamadas IA in/out por WhatsApp y teléfono, multi-idioma | Fuerte en India; precios agresivos |
| [respond.io Voice AI](https://respond.io/blog/whatsapp-ai-voice-agent) | Voice AI Agents sobre llamadas WhatsApp + inbox omnicanal | B2C de alto volumen; buen fit ventas/soporte |
| [Infobip](https://www.infobip.com/docs/whatsapp/whatsapp-business-calling/business-initiated-calling) | CPaaS enterprise: WhatsApp calling + Calls API + IA | SLA enterprise, presencia LatAm |
| [Gupshup](https://partner-docs.gupshup.io/docs/permanent-call-permissions-for-whatsapp-voice) | WhatsApp voice + bots, fuerte en India/LatAm | Docs de permisos permanentes de llamada |
| [DoubleTick](https://docs.doubletick.io/reference/whatsapp-call-public-api) | WhatsApp Call API pública sobre su plataforma | Simple para equipos de ventas WhatsApp-first |
| Zenvia / Botmaker | Plataformas LatAm en español con canales WhatsApp + voz | Soporte local en español |
| [Dapta](https://dapta.ai/) | Voice AI para ventas B2B pensado para LatAm | Español nativo, calificación de leads |

### Voz IA general (PSTN; WhatsApp vía puente Twilio/SIP)

| Plataforma | Precio aprox. | Perfil |
|---|---|---|
| [Vapi](https://vapi.ai) | ~$0.05/min orquestación + proveedores | API-first, máximo control; permite elegir gpt-realtime como modelo |
| [Retell AI](https://retellai.com) | ~$0.07/min | Operación y monitoreo de call centers IA |
| [Bland AI](https://bland.ai) | ~$0.09/min all-in | Outbound masivo de ventas, el más barato a volumen |
| [Synthflow](https://synthflow.ai) | planes por minutos | No-code, para armar rápido sin programar |
| [Lindy](https://lindy.ai) | por tarea | Agentes de negocio con voz entre muchas otras cosas |
| [Pipecat](https://github.com/pipecat-ai/pipecat) / [LiveKit Agents](https://livekit.io) | open source | Frameworks para construirlo vos (lo que hace este repo) |

**Nota de compliance para ventas:** las llamadas salientes por WhatsApp SIEMPRE requieren
el permiso previo del usuario (opt-in explícito, renovable). Para campañas frías eso las
hace inviables por diseño — el flujo correcto es: lead entra por mensaje/anuncio
(click-to-WhatsApp) → pide/acepta la llamada → el agente llama. Además aplican las normas
locales de telemarketing de cada país (en EE.UU./Canadá directamente no hay salientes).

## 5. Costos del MVP (por llamada de 10 min)

| Ítem | Estimado |
|---|---|
| OpenAI gpt‑realtime‑2.1 | ~USD 2–5 |
| WhatsApp saliente (rate card AR, pulsos 6 s) | centavos–pocos USD según tarifa vigente |
| Meta sandbox | USD 0 de plataforma |
| Infra (dev local + túnel) | USD 0 (Fly/Railway ~USD 5/mes si se deploya) |
