# Aprendizajes — Informe diario de rugby uruguayo

Este archivo acumula feedback del usuario sobre los informes diarios para mejorar
las próximas ediciones. Antes de generar un nuevo informe, revisar esta lista.

## Cómo usar este archivo
- Cada vez que el usuario dé feedback sobre un informe (algo salió mal, faltó algo,
  sobró algo, formato incorrecto, fuente no confiable, etc.), agregar una entrada
  nueva abajo con fecha y la lección aprendida.
- Antes de escribir el siguiente informe, releer todas las entradas y aplicarlas.

## Entradas

- 2026-07-04: Primera corrida del informe. Notas del propio proceso (no son
  feedback del usuario, sino observaciones a validar):
  - Las páginas de ESPN Deportes (espn.com.uy, espndeportes.espn.com, espn.cl,
    espn.com.mx) casi siempre devuelven contenido vacío vía fetch directo
    (parecen requerir JS). Conviene apoyarse en los snippets de búsqueda web
    en vez de intentar el fetch directo a ESPN, o buscar la misma noticia en
    Montevideo.com.uy / La Nación / Infobae como alternativa.
  - obcyogc.com (Old Boys oficial) estaba en mantenimiento (solo muestra una
    imagen) el 2026-07-04. Si sigue así, no depender de esa fuente y aclararlo.
  - xn--pearol-xwa.org (Peñarol oficial) devolvió noticias desactualizadas
    (de 2023/2025) pese a pedir las más recientes. Verificar fecha real de
    cada noticia antes de darla por "de las últimas 24 horas".
  - No se encontró una tabla de posiciones del Top 12 Campeonato Uruguayo
    fiable y actualizada a través de fetch/búsqueda (uru.org.uy no expone la
    tabla en texto plano fácil de extraer). Pendiente: buscar una fuente
    estable para esta tabla (¿promiedos.com.ar, flashscore con fetch de API,
    o pedir al usuario un link directo?).
  - El Súper Rugby Américas 2026 terminó el 19/6 (Pampas campeón). Mientras
    no arranque una nueva temporada, Peñarol probablemente seguirá "Sin
    novedades" salvo anuncios de plantel/fichajes.
  - El Torneo Clausura del Top 12 Uruguay arranca el 1/8/2026. Hasta esa
    fecha, Old Boys probablemente tenga poca o ninguna novedad salvo que
    haya anuncios de plantel, lesiones, o actividad institucional.
