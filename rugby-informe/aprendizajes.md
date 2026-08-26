# Aprendizajes — Informe diario de rugby uruguayo

Este archivo acumula feedback del usuario sobre las ediciones del informe diario
(Peñarol Rugby, Old Boys, Los Teros, Los Pumas + tablas de posiciones), para
que cada nueva edición mejore sobre la anterior. Se actualiza cada vez que el
usuario da feedback explícito sobre una respuesta.

Formato de cada entrada:

```
## AAAA-MM-DD
- Feedback del usuario: ...
- Ajuste aplicado / a aplicar: ...
```

## Notas de proceso (no son feedback del usuario, son notas técnicas propias)

- Los resultados de WebSearch a veces resumen con fechas incorrectas o mezclan
  temporadas distintas (ej.: un resultado dado como "23 de agosto de 2026"
  resultó ser en realidad del 23 de agosto de **2025**). Siempre verificar la
  fecha real abriendo la fuente primaria con WebFetch antes de incluir un dato
  en el informe.
- La Súper Rugby Américas 2026 terminó su temporada en junio 2026 (final
  Pampas 26-17 Dogos XV, 19/06/2026). Mientras no arranque una nueva edición,
  no van a aparecer "novedades de la última semana" sobre Peñarol salvo fichajes,
  bajas de DT, etc. — reportar "Sin novedades" es lo correcto si no hay nada
  nuevo, no un fallo de búsqueda.
- No se encontró una tabla de posiciones del Top 12 uruguayo 2026 confiable y
  actualizada (con PJ/PG/PP) en una fuente única. uru.org.uy no publica una
  tabla fácil de extraer vía fetch; considerar pedirle al usuario el link
  directo a la tabla si la conoce, o probar con sitios como 365scores/flashscore
  puntualmente en cada edición.
