# Aprendizajes — Informe Diario Rugby Uruguayo

## Configuración del informe

- **Destinatario:** rugby@itamoa.com
- **Cuenta Gmail remitente:** andresbazzurro@gmail.com
- **Frecuencia:** Diaria
- **Formato:** Markdown → HTML para email
- **Límite temporal de novedades:** últimas 24 horas estrictas

---

## Fuentes confirmadas como útiles

| Fuente | URL | Utilidad |
|--------|-----|----------|
| Sofascore | https://www.sofascore.com | Resultados en tiempo real (confirmó Yacaré 22-36 Peñarol el 30/05) |
| Americas Rugby News | https://www.americasrugbynews.com | Resúmenes semanales SRA, noticias internacionales |
| ESPN Deportes UY | https://www.espn.com.uy | Tabla SRA, resultados, noticias locales |
| ESPN Deportes (internacional) | https://espndeportes.espn.com | Top 12 tabla de posiciones, resultados |
| La Nación (AR) | https://www.lanacion.com.ar | Tabla SRA post-fecha (muy detallada) |
| URU oficial | https://uru.org.uy | Noticias oficiales Los Teros, planteles |
| ABC Color (PY) | https://www.abc.com.py | Noticias sobre Yacaré XV y partidos en Paraguay |
| Peñarol oficial | https://www.peñarol.org | Noticias del club (acceso intermitente) |
| rugbynews.com.uy | https://www.rugbynews.com.uy | Portal local, pero con errores 503 frecuentes |

## Fuentes problemáticas

- `supremacia.uy/tablas.php` → devuelve fútbol, no rugby
- `rugbynews.com.uy` → HTTP 503 frecuente
- `uru.org.uy/campeonato-15` → no muestra tabla directamente, solo noticias

---

## Aprendizajes operativos

### 31 de mayo de 2026 (primer informe)

- La tabla de posiciones del Top 12 Campeonato Uruguayo no está disponible en tiempo real en las fuentes públicas; la última confirmada fue tras Fecha 3 del Torneo Apertura (ESPN). Hay un rezago de ~2 semanas en su publicación online.
- El partido Yacaré vs Peñarol de la Fecha 13 SRA fue el sábado 30/05 a las 20:00 hs locales (23:06 UTC). Resultado: Peñarol 36-22. Los puntos finales de Peñarol en la tabla SRA debieron estimarse (~34 pts) ya que la tabla oficial aún no refleja ese resultado.
- La tabla SRA más actualizada se obtiene desde ESPN (`espn.com.uy` fixtures page) o La Nación.
- Los Teros: la noticia más reciente disponible es del 25/05 (visita a venues RWC 2027 en Australia). Sin novedades en las últimas 24h el 31/05.
- Old Boys: la noticia más reciente disponible es del Fecha 3 del Apertura (victoria 62-0 vs CTM). Sin novedades en las últimas 24h el 31/05.
- Gmail MCP solo permite crear borradores (`create_draft`), no enviar directamente. El usuario debe enviar el borrador desde su cuenta Gmail manualmente, o confirmar para que se envíe.

---

## Feedback recibido

*(Se irá completando con el feedback del usuario)*

