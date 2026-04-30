# Aprendizajes — Informe Diario Rugby Uruguayo

Archivo de registro de feedback recibido y ajustes aplicados al informe diario.

---

## Configuración del informe

- **Destinatario:** rugby@itamoa.com
- **Frecuencia:** Diaria
- **Cobertura:** Peñarol Rugby (SRA), Old Boys (Top 12 URU), Los Teros XV y Teros 7
- **Ventana de noticias:** Últimas 24 horas estrictas. Si no hay novedades → "Sin novedades"
- **Tablas de posiciones:** Siempre incluir, aunque no haya noticias del día

---

## Fuentes prioritarias (por orden de confiabilidad)

1. https://uru.org.uy — URU oficial (a veces devuelve contenido desactualizado en fetch)
2. https://www.americasrugbynews.com — mejor fuente para SRA en inglés
3. https://espndeportes.espn.com — mejor fuente en español para SRA y Top 12
4. https://www.lanacion.com.ar — buena para tablas de posiciones SRA
5. https://www.superrugbyamericas.com — oficial SRA
6. https://www.xn--pearol-xwa.org/categoria/Rugby-218 — Peñarol oficial (a veces requiere fetch directo)
7. https://www.obcyogc.com — Old Boys oficial (503 frecuente, poco confiable para scraping)
8. https://www.rugbynews.com.uy — portal uruguayo (503 frecuente)

---

## Notas técnicas

- `uru.org.uy/campeonato-15` no devuelve datos de la temporada actual correctamente vía fetch.
- `rugbynews.com.uy` suele responder 503 durante el proceso de búsqueda.
- `obcyogc.com` tiene información limitada en fetch; preferir ESPN o búsqueda directa.
- La tabla del Top 12 URU se encuentra mejor en ESPN Deportes (espndeportes.espn.com).
- Los resultados del Top 12 tienen demora de ~1-2 días en indexarse en buscadores.
- El partido Tarucas vs Peñarol (Fecha 9) fue jugado el 27/04 pero publicado como 26/04 en algunos medios.

---

## Formato acordado

- Markdown con tablas HTML para el email
- Fecha en el encabezado
- 3 secciones: Peñarol / Old Boys / Los Teros
- Tablas de posiciones al final (SRA + Top 12)
- Máximo 1 párrafo por novedad
- Links a fuentes al final de cada item
- Equipos del informe destacados en negrita/emoji ⭐ en las tablas

---

## Registro de feedback

| Fecha | Feedback recibido | Ajuste aplicado |
|-------|------------------|-----------------|
| — | — | — |

---

## Historial de informes enviados

| Fecha | Peñarol | Old Boys | Los Teros | Notas |
|-------|---------|----------|-----------|-------|
| 2026-04-30 | Victoria vs Tarucas 34-20 (F9, 27/04) | Sin novedades (F4 no disponible) | Sin novedades | Draft enviado a rugby@itamoa.com |
