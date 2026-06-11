# Aprendizajes — Informe Diario Rugby Uruguayo

## Formato y estructura
- El informe cubre: Peñarol Rugby (Super Rugby Américas), Old Boys (Top 12 URU), Los Teros (XV + 7s).
- Si no hay novedades de las últimas 24 horas para algún equipo, se escribe literalmente "Sin novedades".
- Tablas de posiciones se incluyen siempre (aunque no haya novedades), con la última data disponible y su fecha.
- Formato: Markdown. Links a fuentes al pie de cada ítem. Máximo 1 párrafo por novedad.
- El email se envía a rugby@itamoa.com.

## Fuentes prioritarias (en orden)
1. uru.org.uy — Unión de Rugby del Uruguay (oficial)
2. peñarol.org — Peñarol oficial
3. obcyogc.com — Old Boys oficial (nota: sitio frecuentemente en mantenimiento)
4. espn.com.uy — rugby uruguayo
5. lanacion.com.ar — cobertura Super Rugby Américas
6. infobae.com — cobertura Super Rugby Américas
7. montevideo.com.uy — noticias locales
8. pasionrugby.com.uy — análisis local (bloquea WebFetch con 403)

## Problemas conocidos de fuentes
- obcyogc.com frecuentemente muestra página de mantenimiento — buscar noticias de Old Boys en ESPN o URU.
- pasionrugby.com.uy devuelve HTTP 403 al intentar fetch directo.
- uru.org.uy/campeonato no siempre muestra tabla completa en fetch; usar ESPN para tablas del Top 12.
- espn.com.uy/rugby/calendario/_/liga/11661 devuelve contenido vacío en fetch.
- Para tabla Top 12 usar ESPN notas de resultados por fecha (ej: /16690925/).
- Para Super Rugby Américas tabla: lanacion.com.ar y infobae.com son las mejores fuentes.

## Distinciones importantes
- "Old Boys" del Top 12 Uruguay = Club Old Boys de Montevideo (OBCYOGC). Diferente al "Old Boys" del rugby chileno (ARUSA Top 10). No confundir.
- Teros 7 = Teros Seven masculino (circuito SVNS). Diferente a Teros XV (selección mayor).

## Historial de feedback del usuario
<!-- Agregar feedback recibido aquí -->

## Notas por edición
- 2026-06-11: Primera edición. Tabla Top 12 incompleta (solo top 5 de fecha 6). Tabla Super Rugby Américas con discrepancias menores entre fuentes (La Nacion vs Infobae). Se usaron datos de Infobae (10/6) como más recientes.
