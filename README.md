# 🌿 Jardineando · Pacha Mama

Catálogo interactivo del jardín casero — 40 especies, calendario de eventos y **Timeline de tareas** estilo Tinder con WhatsApp pre-armado por perfil de contacto.

![Jardineando · Pacha Mama](https://img.shields.io/badge/plantas-40-green) ![nativas](https://img.shields.io/badge/nativas_uruguayas-5-blue) ![frutales](https://img.shields.io/badge/frutales-11-orange)

---

## ✨ Qué hace

- **🏡 Frente / 🌳 Fondo** — catálogo con 6 sub-vistas: nombres, podas, ideas nuevas, huerta, calendario anual, acción urgente.
- **📋 Timeline** — tu próxima tarea de jardín en formato newsfeed:
  - Tarjetas swipeable estilo Tinder (→ marcar hecho, ← posponer)
  - Botones: ✅ Hecho · 😴 Posponer (1 día / 3 días / 1 semana / 2 sem / 1 mes / 3 meses / fecha custom) · 💬 WhatsApp
  - WhatsApp con **mensaje pre-armado por perfil de contacto**: jardinero, jornalero multiuso, empresa de piscina, electricista, vivero, leñador
  - Estado guardado en tu navegador (localStorage)
  - Filtros: Activas / Hechas / Pospuestas / Todas

---

## 🚀 Setup rápido (15 minutos al pie)

### Lo que vas a necesitar

| Herramienta | Para qué |
|---|---|
| Python 3 + Pillow | Para regenerar `docs/index.html` |
| Cuenta GitHub (gratis) | Para hostear |
| Claude Code | Para iterar el código con IA |

### Paso 1 — Descomprimir el zip

Te llega un archivo `jardineando-repo.zip`. Descomprimílo donde quieras:

```bash
unzip jardineando-repo.zip
cd jardineando-repo
```

### Paso 2 — Probar el build local

```bash
pip install Pillow
python build.py
```

Eso genera `docs/index.html`. Abrílo en cualquier navegador para ver que funcione:

```bash
# macOS:
open docs/index.html
# Linux:
xdg-open docs/index.html
# Windows:
start docs/index.html
```

### Paso 3 — Subir a GitHub

1. **Crear repo nuevo** en https://github.com/new
   - Nombre: `jardineando-pacha-mama` (o el que quieras)
   - Público o privado, da igual para Pages
   - **NO** inicialices con README (ya tenés uno)

2. **Subir el código** (desde la terminal en la carpeta del proyecto):

   ```bash
   git init
   git add .
   git commit -m "Versión inicial"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/jardineando-pacha-mama.git
   git push -u origin main
   ```

### Paso 4 — Activar GitHub Pages

1. En tu repo en GitHub, andá a **Settings** → **Pages** (en la barra lateral izquierda).
2. En **Source**: elegí **"Deploy from a branch"**.
3. En **Branch**: elegí **`main`** y carpeta **`/docs`** → **Save**.
4. Esperá 1-2 minutos. La URL te aparece arriba en la misma página, algo como:

   ```
   https://TU_USUARIO.github.io/jardineando-pacha-mama/
   ```

✅ **Listo, tu jardín ya está online.**

### Paso 4.5 — Configurar SITE_URL para previews de WhatsApp

**Una sola vez**, abrí `build.py` y editá la constante `SITE_URL` con la URL de GitHub Pages que acabás de obtener (sin barra final):

```python
SITE_URL = "https://TU_USUARIO.github.io/jardineando-pacha-mama"
```

Después corré `python build.py` y hacé `git add . && git commit -m "Configurar SITE_URL" && git push`.

Esto activa los previews de WhatsApp: cuando compartís una tarea, va a aparecer con foto, título y descripción de esa planta específica. Si no lo configurás, los links de tareas no van a tener preview rico (todo lo demás funciona igual).

### Paso 5 — Abrir con Claude Code

[Claude Code](https://claude.com/claude-code) es la CLI de Anthropic para programar con IA en tu terminal/IDE.

```bash
# Instalar (una sola vez)
npm install -g @anthropic-ai/claude-code

# Abrir el proyecto
cd jardineando-pacha-mama
claude
```

Claude Code lee el archivo **`CLAUDE.md`** automáticamente — ya tiene todo el contexto del proyecto y sabe cómo iterar. Probá pedirle cosas como:

> "Quiero que cuando termine una tarea me muestre confeti animado"

> "Agregá un campo 'notas' a cada tarea, editable, que se guarde en localStorage"

> "Cuando una planta tenga floración este mes, mostrame una notificación arriba del Timeline"

### Paso 6 — Ciclo de iteración

Cada vez que cambies algo:

```bash
python build.py                              # regenerá docs/index.html
git add docs/index.html data_*.py *.py       # los cambios
git commit -m "Lo que hayas cambiado"
git push                                     # GitHub Pages actualiza solo en 1-2 min
```

---

## 📂 Estructura del proyecto

```
jardineando-pacha-mama/
├── build.py              ← script principal: ejecutalo para generar docs/
├── data_plants.py        ← catálogo de 40 plantas (editá acá para agregar/cambiar)
├── data_ideas.py         ← ideas nuevas + huerta + contactos default
├── styles.py             ← CSS embebido como string
├── scripts.py            ← JS del Timeline (estado, swipe, modales, WhatsApp)
├── images/               ← 62 fotos del jardín
├── docs/
│   └── index.html        ← ⚡ archivo final de 13MB (lo que GitHub Pages sirve)
├── README.md             ← este archivo
├── CLAUDE.md             ← contexto para Claude Code
└── .gitignore
```

---

## 🔧 Cómo modificar cosas comunes

### Agregar una planta

Editá `data_plants.py` y agregá un dict al final del array `PLANTS`. Copiá la estructura de cualquier otra planta. Después: `python build.py && git push`.

### Marcar una tarea como urgente (que aparezca en el Timeline)

En `data_plants.py`, en la planta correspondiente, cambiá el campo `urgency` de `None` a:

```python
"urgency": {
    "priority": "alta",  # o "media" / "baja"
    "action": "Lo que hay que hacer",
    "when": "Junio 2026",
    "due_month": 6,
    "due_year": 2026,
},
```

### Cargar tus contactos de WhatsApp

**Acá no toques código** — abrí el sitio, andá a la pestaña Timeline, click en **📞 Mis contactos** y completá los teléfonos. Se guarda en tu navegador (localStorage), no se sube al repo. **Tus números nunca salen de tu dispositivo.**

### Cambiar las plantillas de mensajes por defecto

Si querés que la plantilla por defecto venga distinta para todos los usuarios (no solo para vos), editá `DEFAULT_CONTACTS` en `data_ideas.py`. Usá `{task}` donde quieras que aparezca el texto de la tarea.

---

## 🤖 Workflow recomendado con Claude Code

1. Pedile a Claude lo que querés cambiar (ej: "agregá un botón para exportar las tareas hechas como PDF")
2. Claude edita los archivos `.py` y vos revisás los cambios
3. Corré `python build.py` para regenerar
4. Abrí `docs/index.html` localmente y verificá
5. Si te gusta, `git push` y queda online en 1-2 min

Claude Code ya tiene contexto completo del proyecto vía `CLAUDE.md`.

---

## 🐛 Troubleshooting

**"GitHub Pages no muestra nada"** — Esperá 2-3 minutos después del primer push. Si sigue sin funcionar, verificá que en Settings → Pages la branch sea `main` y la carpeta `/docs`. Hard-refresh con Ctrl+Shift+R.

**"El sitio carga muy lento"** — Son 13MB porque las imágenes están embebidas en el HTML (para que sea un solo archivo). Si querés optimizar, podés mover imágenes a `docs/images/` y referenciarlas con paths relativos — pedile a Claude Code que lo haga.

**"No me funciona el WhatsApp"** — Asegurate de haber cargado los teléfonos en **📞 Mis contactos** con código de país (ej: `+598 99 123 456`).

**"Perdí mis tareas marcadas como hechas"** — Borraste la caché del navegador o estás en otro dispositivo. El estado vive en localStorage del navegador. Para sincronización entre dispositivos haría falta un backend — Claude Code te puede armar uno con Firebase o similar.

---

## 📜 Licencia

Tu jardín, tus reglas. Hacé fork, modificá, compartí. 🌱
