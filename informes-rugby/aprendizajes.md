# Aprendizajes — Informe diario de rugby uruguayo

Este archivo guarda feedback del usuario sobre los informes diarios para no repetir errores.
Se actualiza cada vez que el usuario da una corrección o preferencia nueva.

## Reglas fijas (no negociables, ya definidas en el prompt original)

- Ventana: solo novedades de las últimas 24 horas.
- Alcance: Peñarol Rugby (SRA), Old Boys (Top 12), Los Teros (XV y 7s), Los Pumas.
- Si no hay novedad real y verificable en la ventana de 24hs: escribir literalmente "Sin novedades". No rellenar con contexto viejo.
- No incluir otros equipos salvo en las tablas de posiciones (para contextualizar).
- No incluir rugby internacional que no involucre directamente a Peñarol, Old Boys o Los Teros.
- Markdown, fecha arriba, una sección por tema, máx. 1 párrafo por novedad, links al final de cada item.
- Incluir tabla de Súper Rugby Américas y tabla del Top 12 Uruguayo actualizadas.
- Destino: rugby@itamoa.com

## Notas operativas (aprendidas durante la ejecución, no del usuario)

- Las webs de ESPN (espn.com.uy / espn.com.mx / espndeportes.espn.com) son mayormente JS-rendered:
  WebFetch casi siempre devuelve contenido vacío. Conviene usar WebSearch para extraer el dato
  desde el snippet indexado, o buscar la misma nota en montevideo.com.uy / La Nación / uru.org.uy.
- uru.org.uy publica sus tablas de posiciones como imágenes (tabla.jpg), no como texto: no se
  pueden extraer con WebFetch. Para el Top 12 conviene reportar resultados de fase
  eliminatoria (semis/final) en vez de inventar una tabla de puntos que no se puede verificar.
- Cuidado con el ruido de "Peñarol" a secas: la mayoría de las búsquedas devuelven noticias del
  Peñarol de fútbol (Liga AUF Uruguaya), no de Peñarol Rugby. Siempre agregar "rugby" o
  "Súper Rugby Américas" al query y descartar resultados de fútbol.
- Cuidado con el sitio "supremacia.uy": pese al nombre, es de fútbol, no de rugby.
- Ambiguar fechas exactas de partidos ("se jugará este fin de semana") es normal en las notas
  previas; si no se encuentra la fecha exacta de publicación de la nota con el resultado, mejor
  encuadrar como "este fin de semana" en vez de afirmar una fecha/hora específica no verificada.

## Feedback del usuario (historial)

_(Vacío por ahora — acá se agregan las correcciones que el usuario vaya dando sobre informes anteriores, con fecha.)_

<!-- Formato sugerido para nuevas entradas:
### YYYY-MM-DD
- Feedback: ...
- Ajuste aplicado: ...
-->
