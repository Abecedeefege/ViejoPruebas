# 2026-04-24 — AI radar daily briefing

## Qué se pidió

Configurar un flujo donde Claude actúe como analista de tendencias AI: escanear fuentes (HN, Product Hunt, GitHub trending, Reddit, HF, lab blogs, X) filtradas por los proyectos del usuario, y mandar un briefing por Gmail a `airadar@itamoa.com`.

## Contexto del usuario (recurrente — usar como filtro en futuras sesiones)

- **BoopKids** — app para chicos. Intereses: subscription analytics, ideas de tráfico/installs, ads attribution.
- **Consultoría** — digital marketing y growth.
- **Alexa Skills** — AWS Lambda + OpenAI. Voice AI y agentes conversacionales.
- **portalgarzon.com** — turismo local José Ignacio / Laguna Garzón. Hyperlocal geo.
- **Monetización online.**
- **findmetea.com** — recomendaciones de té.
- **Obsesión explícita** — agentes autónomos con mínima intervención humana.

## Formato del briefing (estable)

- **Subject:** `AI radar — DD/MM`
- **Top 5** — ranking por relevancia. Cada item: qué es (1 oración), link, por qué importa (ángulo a proyecto), dificultad (fácil/media/difícil), autonomía (1-5).
- **Agentes autónomos top 3** — solo cosas hands-off.
- **Menciones rápidas** — 5-10 bullets.
- **Reglas:** máx 8 links totales, calidad > cantidad, 🎯 para ideas construibles en < 1 semana, no inventar si el día es flojo.

## Qué se hizo

- Scan en paralelo de HN (front + Show), GitHub trending (Py + TS), Product Hunt, HF Spaces.
- Búsquedas targeted: Claude releases, MCP releases, voice AI, indie hackers con MRR, AppsFlyer/Adjust, Alexa + OpenAI.
- Borrador del briefing con 5 items top, 3 agentes, 7 menciones.
- Intento de draft en Gmail a `airadar@itamoa.com` — **falló**: el MCP de Gmail requiere re-autorización (token expirado). Guardado el HTML completo en `2026-04-24-ai-radar-email.html` para enviar manualmente o reintentar.

## Aprendizajes

### Qué funcionó
- **HN Algolia API** (`hn.algolia.com/api/v1/search?tags=front_page&numericFilters=created_at_i>...`) funciona cuando `news.ycombinator.com/front` devuelve 503.
- **old.reddit.com** también está bloqueado (no solo www). Reddit queda fuera de alcance con WebFetch — habría que usar un MCP de Reddit o buscar contenido de Reddit vía WebSearch indirecto.
- **GitHub trending + HF Spaces trending + Product Hunt** son las fuentes más ricas y accesibles con WebFetch.
- Paralelizar WebFetch (hasta 7-8 en una sola respuesta) da un scan completo en ~20s.

### Qué no funcionó / limitaciones
- `www.reddit.com` y `old.reddit.com` bloqueados por WebFetch.
- `news.ycombinator.com/front` → 503. Usar la API de Algolia siempre.
- No hay `mcp__Gmail__get_me` — hay que pedirle el email al usuario explícitamente (o leerlo del repo si lo documentamos acá).
- MCP de PushNotification y labeling de Gmail se desconectaron mid-session. No confiar en que estén disponibles.
- **SMTP outbound bloqueado en el sandbox** (puertos 25/465/587/2525 todos timeout). HTTPS sí funciona. Para enviar desde este sandbox hace falta API HTTP (Resend, Mailgun, Postmark). El Gmail MCP NO expone `send`, solo `create_draft`. App Passwords de Gmail no sirven desde acá (sí desde la máquina del usuario o GitHub Actions).
- Verificado el 24/04: `api.resend.com` 200, `api.mailgun.net` 200, `api.postmarkapp.com` 302 — todos reachable.

### Patrones reutilizables
- **Filtro de relevancia:** no forzar ángulo cuando no aplica (el usuario lo pidió explícito en la sesión). Es mejor omitir que estirar.
- **Ejemplos concretos por proyecto:** para cada item del top 5, aterrizar al menos 1-2 proyectos del usuario con un caso de uso específico (no genérico tipo "útil para cualquier app").
- **🎯 dispensar con criterio:** solo si el MVP se puede montar en < 1 semana por una sola persona con Claude Code.

## Feedback del usuario

1. **Email destino:** `airadar@itamoa.com` (guardar en preferencias de sesión).
2. **Sender propuesto:** `agency@itamoa.com`.
3. **Más ejemplos por proyecto** en cada item. Incluir 1, 2, o todos los proyectos que apliquen.
4. **No forzar** — si no aplica a ningún proyecto, dejarlo vacío.
5. **Documentar aprendizajes** en este repo tras cada sesión (origen de este archivo).
6. **CRÍTICO — investigar antes de proponer.** El usuario marcó (con razón) que propuse SMTP sin verificar si el sandbox lo permitía. Resultado: él generó un Gmail App Password, lo compartió, y después descubrimos que SMTP estaba bloqueado. Regla permanente: **antes de proponer una solución que requiera trabajo o secretos del usuario, testear conectividad / disponibilidad de la dependencia desde este entorno**. Es un costo barato comparado con hacer perder tiempo + pedir un secreto inutilizable.

## Para futuras sesiones (AI radar recurrente)

- Mandar draft directo a `airadar@itamoa.com` sin preguntar.
- Commit del briefing enviado acá también (`docs/sessions/YYYY-MM-DD-ai-radar.md`) para tener historial buscable — útil para detectar repetidos o tendencias multi-día.
- Evitar recomendar lo mismo dos días seguidos salvo que haya novedad real.
- Si un item ya apareció, marcar como "ya visto DD/MM" en vez de repetir.
- Probar fuentes adicionales la próxima vez: Latent Space, Ben's Bites, TLDR AI (RSS si están), Replicate trending.
- Buscar un MCP de Reddit o de X/Twitter para desbloquear esas dos fuentes.
