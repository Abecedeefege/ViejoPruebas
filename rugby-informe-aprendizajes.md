# Aprendizajes — Informe Diario de Rugby Uruguayo

Este archivo acumula feedback del usuario (andresbazzurro@gmail.com) sobre los informes
diarios de rugby uruguayo, para aplicarlo en las próximas ediciones. Se actualiza cada vez
que el usuario da feedback explícito sobre una entrega.

## Formato acordado
- Markdown, fecha arriba, una sección por: Peñarol Rugby, Old Boys, Los Teros (XV y 7s), Los Pumas.
- Tablas de posiciones: Súper Rugby Américas y Top 12 Campeonato Uruguayo.
- Si no hay novedades de las últimas 24h sobre alguno de los tres primeros temas, escribir
  literalmente "Sin novedades". No inventar ni rellenar.
- No incluir rugby internacional que no involucre directamente a Peñarol, Old Boys o Los Teros
  (Los Pumas es la excepción explícita: sí se incluyen).
- Máximo 1 párrafo por novedad, con links a fuentes al final de cada item.
- Destinatario del envío: rugby@itamoa.com

## Fuentes que funcionaron bien
- WebSearch con queries específicas de fecha (ej. "Uruguay Rumania resultado 11 julio 2026")
  da mejores resultados que queries genéricas de "noticias julio 2026".
- Wikipedia (ej. "20XX Super Rugby Americas season") tiene tablas de posiciones finales limpias
  y confiables cuando la temporada ya terminó.
- Fuentes cruzadas en distintos idiomas (prensa rumana para el partido de Los Teros) sirvieron
  para confirmar un resultado dudoso.

## Fuentes problemáticas / limitaciones conocidas
- WebFetch usa un modelo resumidor con conocimiento limitado que a veces:
  - Confunde 2026 con "fecha futura que no ocurrió".
  - Confunde rugby con fútbol en sitios uruguayos (uru.org.uy vs. sitios de fútbol).
  - Devuelve contenido cacheado/viejo (ej. tablas de 2024) sin avisar que está desactualizado.
  - Siempre pedirle que reporte la fecha de publicación del artículo para detectar contenido viejo.
- obcyogc.com (sitio oficial de Old Boys) estuvo "en mantenimiento" el 12/07/2026 — revisar si
  ya está activo en próximas corridas.
- No se encontró una fuente confiable con la tabla de posiciones 2026 del Top 12 Campeonato
  Uruguayo (uru.org.uy no la mostraba en la portada, rugbynews.com.uy dio 503, genrugby.com no
  tiene sección específica de Uruguay). Pendiente: probar https://uru.org.uy/campeonato-15
  directamente en el navegador o buscar un feed/API alternativo.
- Herramienta de email: el conector de Gmail disponible en esta sesión solo tiene
  `create_draft` (no hay un tool de "enviar" directo). El informe se deja como borrador
  dirigido a rugby@itamoa.com; falta enviarlo manualmente o conseguir un tool de envío.

## Feedback del usuario (agregar entradas nuevas abajo, con fecha)
_(vacío por ahora — completar cuando el usuario dé feedback sobre una entrega)_
