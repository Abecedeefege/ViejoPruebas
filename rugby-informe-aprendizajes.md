# Aprendizajes – Informe Diario Rugby Uruguayo

## Fuentes confiables

| Fuente | URL | Utilidad |
|--------|-----|----------|
| La Nación (AR) | lanacion.com.ar | Tabla SRA post-fecha, muy consistente |
| Americas Rugby News | americasrugbynews.com | Resúmenes por ronda SRA, tabla actualizada |
| ESPN Deportes | espndeportes.espn.com | Artículos por fecha del Top 12 uruguayo (ej. `/id/166xxxxx/`) |
| El Telégrafo (Paysandú) | eltelegrafo.com | Resultados del interior, especialmente Trébol vs equipos visitantes |
| Sofascore | sofascore.com | Resultados en vivo / confirmación de marcadores |
| Montevideo.com.uy | montevideo.com.uy | Noticias generales de rugby uruguayo |
| Infobae | infobae.com | Novedades Teros 7 / SVNS / calendarios internacionales |
| Confederación Brasileña de Rugby | brasilrugby.com.br | Partido Cobras vs Peñarol (previas) |
| GDA – Grupo de Diarios América | gda.com | Artículos de fecha a fecha del Top 12 |

## Fuentes con problemas

| Fuente | Problema |
|--------|---------|
| Wikipedia (es/en) | HTTP 403 – no accesible vía WebFetch |
| rugbynews.com.uy | HTTP 503 – caída frecuente |
| supremacia.uy | Solo fútbol, no rugby |
| uru.org.uy/noticias | HTML cargado dinámicamente, WebFetch devuelve contenido incompleto |
| Flashscore | Contenido dinámico (JS), no accesible vía WebFetch |

## Patrones de búsqueda eficaces

- Para tabla SRA: buscar `"Así quedó la tabla" Super Rugby Americas fecha [N] [año]`
- Para resultados SRA: buscar `"Super Rugby Americas" round [N] summary [año]` en inglés
- Para Top 12 por fecha: buscar `espndeportes.espn.com rugby "fecha [N]" "top 12" campeonato uruguayo [año]`
- Para Teros 7: buscar `"Los Teros 7" OR "Teros 7's" SVNS [etapa/ciudad] [año]`
- Para resultado puntual: Sofascore o buscar `[equipo1] [equipo2] resultado [fecha DD de mes]`

## Notas por informe

### 11/05/2026
- La tabla del SRA tras fecha 10 tiene leve discrepancia entre La Nación y Americas Rugby News (1-3 pts). Se usa versión ARN para informe ya que puede incluir bonus points más finos.
- La tabla del Top 12 más reciente disponible online era la de fecha 3 (ESPN, 20/04/2026). Fechas 4, 5 y 6 no tenían artículo ESPN indexado. La próxima vez conviene buscar el ID de artículo ESPN buscando `espndeportes rugby campeonato uruguayo fecha [N] 2026`.
- Trébol vs Old Boys de fecha 6 (10/05) fue confirmada por El Telégrafo de Paysandú.
- Resultado Cobras vs Peñarol de fecha 11 SRA (10/05) confirmado solo por Sofascore (35-12 Peñarol).
- Los Teros XV y Teros 7: sin novedades en últimas 24h el 11/05.

## Feedback recibido
*(vacío – completar al recibir feedback del usuario)*
