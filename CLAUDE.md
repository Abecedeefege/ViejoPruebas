# CLAUDE.md — Contexto del proyecto para Claude Code

## Qué es esto

Sitio estático de un jardín casero en Montevideo, Uruguay. Catálogo de 40 plantas (frente + fondo) con:
- Información detallada por especie
- Calendario anual (floración / fructificación / poda)
- Ideas para sumar plantas nuevas
- Catálogo de huerta
- **Timeline de tareas** estilo Tinder con WhatsApp pre-armado por contacto

## Stack y arquitectura

**Build-time:** Python 3 con Pillow para optimizar e incrustar imágenes como base64.
**Runtime:** HTML5 + CSS + JS vanilla — sin frameworks, sin build step en el browser.
**Hosting:** GitHub Pages servido desde `docs/index.html`.
**Estado del cliente:** `localStorage` (no hay backend).

### Flujo de build

```
data_plants.py + data_ideas.py
       ↓
   build.py
       ↓ (lee imágenes desde images/, las codifica base64,
          genera HTML con CSS de styles.py y JS de scripts.py,
          inyecta TASKS y DEFAULT_CONTACTS como JSON globales)
       ↓
docs/index.html  ← un único archivo monolítico de ~13MB
```

### Archivos clave

| Archivo | Qué contiene | Cuándo tocarlo |
|---|---|---|
| `data_plants.py` | Array `PLANTS` con 40 dicts | Agregar/editar plantas, cambiar urgencias |
| `data_ideas.py` | `NEW_IDEAS_*`, `HUERTA`, `HUERTA_LOCATION_IDEAS`, `DEFAULT_CONTACTS` | Editar ideas o defaults de contactos |
| `build.py` | Render HTML, generación de tareas, helpers | Cambiar layout/estructura de páginas |
| `styles.py` | Todo el CSS como string raw | Cambios visuales |
| `scripts.py` | Todo el JS como string raw | Lógica del Timeline, modales, swipe |
| `images/` | Fotos del jardín (62 archivos) | Agregar fotos nuevas |
| `docs/index.html` | Output del build — **NO editar a mano** | Generado siempre por `python build.py` |

### Modelo de datos — Tarea

Las tareas viven en el JS como `const TASKS = [...]` (inyectado por build.py desde `generate_tasks_from_plants`).

```javascript
{
  id: "plant-B-30",                    // único; usado como key en localStorage
  kind: "plant_action",
  plant_codes: ["B-30", "B-35"],       // ids del catálogo
  plant_common: "Durazno",
  plant_zone: "fondo",                 // "frente" | "fondo"
  plant_photo: "b30.jpg",              // referencia al objeto IMG
  title: "Poda invernal urgente",
  description: "Durazno (B-30, B-35) — Poda invernal urgente.",
  priority: "alta",                    // "alta" | "media" | "baja"
  due_label: "Junio-julio 2026",
  due_month: 6,
  due_year: 2026,
  suggested_contact: "jardinero",      // id de contacto sugerido (puede ser null)
}
```

### Estado de tareas (localStorage)

Clave: `jardineando_task_states_v1`. Valor: objeto `{taskId: {status, snoozed_until, completed_at}}`.

```javascript
{
  "plant-B-30": {
    status: "active" | "done" | "snoozed",
    snoozed_until: "2026-06-15T00:00:00.000Z" | null,
    completed_at: "2026-05-15T14:30:00.000Z" | null
  }
}
```

Lógica:
- Si `status === "snoozed"` y `snoozed_until` ya pasó, la tarea vuelve automáticamente a `active` al renderizar.
- "Reactivar" (botón en tareas done/snoozed) limpia todo y vuelve a active.

### Contactos (localStorage)

Clave: `jardineando_contacts_v1`. Valor: array idéntico en estructura a `DEFAULT_CONTACTS` de `data_ideas.py`:

```javascript
[
  { id, name, icon, phone, default_template }
]
```

`default_template` puede contener `{task}` que se reemplaza con `${title} — ${plant_common} (${plant_codes})` al abrir el modal.

URL de WhatsApp: `https://wa.me/PHONE?text=ENCODED_MESSAGE` donde PHONE es el teléfono sin signos (regex `[^0-9]` se reemplaza por vacío).

### Swipe gestures

Implementado en `setupSwipe(card)` (scripts.py). Soporta touch + mouse:
- `>100px` derecha → marcar hecho (anima `swipe-out-right`)
- `>100px` izquierda → abrir modal snooze
- `<100px` → vuelve a posición
- Ignora si el target es un `<button>` (para que los botones funcionen)
- Distingue swipe horizontal vs scroll vertical en los primeros 12px

## Workflow para iterar

1. Editar `.py` (data o build/styles/scripts)
2. Correr `python build.py`
3. Abrir `docs/index.html` localmente para verificar
4. `git add . && git commit && git push` → GitHub Pages actualiza automáticamente

## Convenciones

- **No editar `docs/index.html` a mano** — siempre regenerar con `python build.py`
- **Al cambiar lógica del Timeline**, editar `scripts.py` (no `build.py`)
- **Al cambiar look & feel**, editar `styles.py`
- **Al cambiar estructura de zonas / sub-tabs**, editar `build.py`
- **Strings en español** — todo el sitio es es-UY
- **Spanish localized dates** — usar `toLocaleDateString('es-UY', ...)`
- **Sin dependencias externas en runtime** — solo Google Fonts vía `@import`. Todo el resto inline.

## Ideas para futuras mejoras

Estas son ideas que el usuario podría querer pedirte:

### Storage / Sync
- Sincronizar estado entre dispositivos (Firebase / Supabase / Pocketbase)
- Exportar / importar estado como JSON
- Backup automático del estado a un Gist privado

### Notificaciones
- Service worker + Notification API para recordar tareas con `due_date` cercana
- Banner arriba del Timeline cuando hay tareas vencidas

### Más datos en cada planta
- Fotos múltiples (galería swipe) — ahora solo `main_photo` y `loc_photo`
- Histórico de podas / cuidados realizados (con fecha y notas)
- Notas libres por planta (editables desde la UI)

### Timeline avanzado
- Repetición de tareas (ej. "regar lavanda cada 7 días")
- Tareas custom creadas desde la UI (no solo derivadas de plantas)
- Drag-and-drop para reordenar
- Búsqueda/filtro por planta o por contacto sugerido

### Optimización
- Mover imágenes a `docs/images/` (paths relativos) en lugar de base64 inline
  → reduce tamaño del HTML de 13MB a ~50KB y permite caché del browser
- Code splitting: cargar timeline.js solo cuando se entra a esa pestaña
- Service worker para cachear el sitio offline

### Visualizaciones
- Mapa del jardín con coords aproximadas de cada planta (clickeable)
- Timeline cronológico (eje horizontal con meses) con todas las tareas

## Cosas a NO hacer

- ❌ No introducir frameworks (React, Vue, etc) — la simplicidad es un feature
- ❌ No usar `<form>` ni `submit` events — el usuario reportó que en Claude Artifacts dan problema
- ❌ No agregar fetch a APIs externas sin avisar — el sitio debe funcionar offline
- ❌ No subir teléfonos al repo — los contactos viven solo en localStorage
- ❌ No cambiar estructura de `docs/` — GitHub Pages depende de eso
