# 📞 voicecall — "Llamame y peloteamos una idea"

Web + agente de voz: escribís tu número en la web y un agente con **OpenAI Realtime
(gpt-realtime-2.1)** te llama por **WhatsApp** para charlar. Sin Twilio ni intermediarios:
directo contra la **WhatsApp Business Calling API** de Meta (Cloud API) con
[Pipecat](https://github.com/pipecat-ai/pipecat) manejando el audio WebRTC.

```
┌──────────┐  POST /api/call   ┌─────────────┐  Graph API (permiso + POST /calls con SDP offer)
│ web      │ ────────────────► │ agent       │ ─────────────────────────────► Meta / WhatsApp
│ Next.js  │  ◄─ polling ────  │ FastAPI     │ ◄── webhooks calls/messages ──  │
│ (Vercel) │                   │ + Pipecat   │                                 ▼
└──────────┘                   │   WebRTC ◄──┼──── audio Opus (SRTP) ────► tu celular 📱
                               │   ▲         │
                               │   └─ OpenAI Realtime (speech-to-speech, WebSocket)
                               └─────────────┘
```

## Estructura

| Carpeta | Qué es |
|---|---|
| `agent/` | Backend de voz (Python 3.11, FastAPI + Pipecat). Webhooks de Meta, llamadas salientes/entrantes, puente audio ↔ OpenAI Realtime. |
| `web/` | Frontend (Next.js 15). Form de número + estado de la llamada. Deploy pensado para Vercel. |
| `docs/` | `setup-meta.md` (paso a paso de cuentas) y `investigacion.md` (investigación completa + proveedores). |

## Quickstart (dev local)

Requisitos: Python 3.11+, [uv](https://docs.astral.sh/uv/), Node 20+, una cuenta en
[developers.facebook.com](https://developers.facebook.com) y una API key de OpenAI con billing.

**1. Configurar Meta (una vez, ~15 min):** seguí [`docs/setup-meta.md`](docs/setup-meta.md).
Con el **número de prueba** del panel alcanza — no hace falta verificación de negocio para el sandbox.

**2. Backend de voz:**

```bash
cd voicecall/agent
uv venv && uv pip install -e ".[dev]"
cp .env.example .env   # completar tokens
uv run uvicorn voicecall_agent.main:app --host 0.0.0.0 --port 8000
```

**3. Túnel para webhooks** (en otra terminal):

```bash
cloudflared tunnel --url http://localhost:8000
# la URL https://xxx.trycloudflare.com va en el panel de Meta como
# webhook: https://xxx.trycloudflare.com/webhooks/whatsapp
```

**4. Web:**

```bash
cd voicecall/web
npm install && cp .env.example .env.local   # AGENT_URL + AGENT_API_TOKEN
npm run dev   # http://localhost:3000
```

**5. Probar:** escribí tu número → `Llamame por WhatsApp` → la primera vez llega un
pedido de permiso a tu WhatsApp → aceptás → te llama el agente y charlan.
También podés llamar VOS al número de prueba desde WhatsApp: el bot atiende.

## Tests

```bash
cd voicecall/agent && uv run pytest      # 36 tests: webhooks, permisos, máquina de estados, API
cd voicecall/web && npm run build        # typecheck + build
```

## Seguridad y límites

- `ALLOWED_DESTINATIONS`: allowlist de números a los que se puede llamar (vacío = nadie). Evita que un tercero te queme crédito.
- `AGENT_API_TOKEN`: la web habla con el agente con bearer token (server-side only).
- Webhooks validados con `X-Hub-Signature-256` (`META_APP_SECRET`).
- `MAX_CALL_MINUTES` corta la llamada por watchdog.
- Sandbox de Meta: 25 pedidos de permiso/día, llamadas solo a destinatarios de prueba registrados; con permiso vigente, hasta 5 llamadas/24h por usuario (dura 7 días).

## Costos aproximados

| Ítem | Costo |
|---|---|
| OpenAI gpt-realtime-2.1 | ~USD 0,2–0,5 por minuto de conversación ($32/M tokens audio in, $64/M out) |
| WhatsApp llamada saliente | rate card por país, pulsos de 6 s (entrantes: gratis) |
| Meta sandbox / número de prueba | sin costo de plataforma |

## Producción (siguiente etapa)

Para salir del sandbox: verificación de negocio en Meta + número real con límite de
mensajería ≥2.000/día, o migrar el transporte a **Twilio WhatsApp Business Calling**
(GA desde jul-2025) manteniendo el mismo pipeline. Detalle en
[`docs/investigacion.md`](docs/investigacion.md).
