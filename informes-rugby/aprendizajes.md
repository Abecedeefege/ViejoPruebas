# Aprendizajes — Informe diario de rugby uruguayo

Este archivo acumula feedback del usuario (andresbazzurro@gmail.com) sobre las
ediciones del informe diario de rugby (Peñarol Rugby, Old Boys, Los Teros,
Los Pumas), para no repetir errores en próximas ejecuciones.

## Cómo se usa
Cada vez que el usuario dé feedback sobre una entrega, agregar una entrada
abajo con: fecha, qué se corrigió, y la regla concreta a aplicar de ahí en
más. Antes de generar un nuevo informe, releer esta lista.

## Entradas

### 2026-07-27 (primera ejecución)
- No existía este archivo; se creó en esta corrida.
- Limitaciones detectadas en las fuentes/herramientas disponibles que
  conviene tener presentes:
  - `WebFetch` no puede renderizar espn.com.uy / espn.com.ar / espndeportes
    (devuelve contenido vacío, sitio con carga por JS). Para ESPN conviene
    usar `WebSearch` con `allowed_domains` y cruzar con al menos otra fuente
    antes de dar un dato (marcador, fecha) por confirmado.
  - `WebFetch` a obcyogc.com (Old Boys oficial) devolvió una imagen de
    "sitio en mantenimiento" el 2026-07-27. Revisar si sigue caído en
    próximas corridas.
  - El resumen automático de `WebSearch` a veces mezcla resultados de años
    distintos (ej. confundió la final del Torneo Apertura 2026 Old Boys vs
    Old Christians con la final del Campeonato Uruguayo de noviembre 2025,
    que tuvo un marcador distinto). Regla: cuando un dato clave (marcador,
    fecha exacta) solo aparece en el resumen sintetizado y no se puede
    corroborar con un fetch directo a la fuente primaria, tratarlo como no
    confirmado y no incluirlo, o aclarar la incertidumbre.
  - No se encontró una tabla de posiciones del Top 12 uruguayo confiable y
    verificada como "actual" al 2026-07-27 (supremacia.uy solo tiene fútbol,
    365scores mostró URBA Top 14 argentino, pasionrugby.com.uy devolvió
    403). Pendiente: buscar una fuente estable para esta tabla.
  - El Súper Rugby Américas 2026 ya terminó en junio (Pampas campeón); no
    tiene sentido buscar "novedades de las últimas 24h" de ese torneo hasta
    que arranque la próxima temporada — su sección probablemente diga
    "Sin novedades" la mayoría de los días hasta entonces.
  - La herramienta Gmail conectada en esta sesión solo expone
    `create_draft` / `update_draft` (no hay una acción de "enviar"). El
    informe se dejó como borrador dirigido a rugby@itamoa.com en vez de
    enviarse. Si el usuario quiere que se envíe de verdad, revisar si hay
    forma de habilitar el envío o si hay que pedirle que lo envíe él
    manualmente desde el borrador.
