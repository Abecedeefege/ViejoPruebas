# Setup de Meta / WhatsApp Cloud API (sandbox, sin verificación de negocio)

Objetivo: dejar un **número de prueba** de WhatsApp con **calling habilitado** apuntando
al agente. 15–20 minutos.

## 1. Crear la app en Meta

1. Entrá a [developers.facebook.com](https://developers.facebook.com) → **My Apps** → **Create App**.
2. Tipo **Business**. Nombre: lo que quieras (ej: `voicecall-sparring`).
3. En el dashboard de la app, agregá el producto **WhatsApp** (Set up).
4. Esto crea una **WhatsApp Business Account (WABA) de prueba** con un **número de prueba** gratis.

## 2. Datos que van al `.env` del agente

En **WhatsApp → API Setup**:

| Variable | De dónde sale |
|---|---|
| `WHATSAPP_ACCESS_TOKEN` | El token temporal del panel (24 h) o mejor: un **System User token** permanente (Business Settings → System Users → Generate token con permisos `whatsapp_business_messaging` y `whatsapp_business_management`). |
| `WHATSAPP_PHONE_NUMBER_ID` | "Phone number ID" del número de prueba (NO es el número de teléfono). |
| `WHATSAPP_WABA_ID` | "WhatsApp Business Account ID". |
| `META_APP_SECRET` | App Settings → Basic → App Secret. |
| `WHATSAPP_VERIFY_TOKEN` | Lo inventás vos; tiene que coincidir con el del paso 4. |

## 3. Registrar tu celular como destinatario de prueba

En **API Setup → To**: agregá tu número personal de WhatsApp (te llega un código por
WhatsApp). El número de prueba solo puede interactuar con destinatarios registrados (hasta 5).

## 4. Configurar webhooks

1. Levantá el agente local (`uvicorn ... --port 8000`) y el túnel:
   `cloudflared tunnel --url http://localhost:8000` → te da `https://xxx.trycloudflare.com`.
2. En la app de Meta: **WhatsApp → Configuration → Webhook**:
   - Callback URL: `https://xxx.trycloudflare.com/webhooks/whatsapp`
   - Verify token: el mismo que pusiste en `WHATSAPP_VERIFY_TOKEN`.
   - **Verify and save** (el agente responde el challenge).
3. En **Webhook fields**, suscribite a: **`calls`** y **`messages`**.

> El túnel de cloudflared cambia de URL en cada corrida; si lo reiniciás, actualizá la
> Callback URL. Para algo estable: `cloudflared` con dominio propio, o deploy en Fly/Railway.

## 5. Habilitar calling en el número

En **WhatsApp → API Setup** (o Phone numbers → Settings → Calling, según versión del panel):
activá **Calling** para el número de prueba, con llamadas entrantes permitidas.
Los números de prueba están **exentos** del requisito de producción (límite de mensajería
de 2.000 destinatarios/día).

> Si no ves la opción de calling, verificá que la app tenga la Cloud API actualizada
> (Graph v23+) y que el número sea el de prueba de la WABA de la app.

## 6. Probar

1. **Entrante:** desde tu WhatsApp, llamá al número de prueba → el bot atiende.
2. **Saliente:** `curl -X POST http://localhost:8000/calls -H "Authorization: Bearer $AGENT_API_TOKEN" -H "Content-Type: application/json" -d '{"to":"+549XXXXXXXXXX"}'` → te llega el pedido de permiso → aceptás → te llama.

## Límites del sandbox (Meta)

- 25 pedidos de permiso por día / 100 por semana.
- 1 pedido de permiso por usuario cada 24 h (2 por semana); se resetea si hay llamada conectada.
- Permiso aceptado: dura 7 días, hasta 5 llamadas por 24 h a ese usuario.
- Llamadas salientes **no disponibles** hacia EE.UU., Canadá, Egipto, Nigeria, Turquía y Vietnam.
