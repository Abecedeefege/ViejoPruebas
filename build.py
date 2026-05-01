"""
Jardineando · Pacha Mama — Build script
Genera docs/index.html con el catálogo + timeline + ideas.

Ejecución:
    python build.py

Salida:
    docs/index.html (subir a GitHub Pages)
"""

import base64
import json
import html as html_mod
from io import BytesIO
from pathlib import Path
from PIL import Image

from data_plants import PLANTS
from data_ideas import (
    NEW_IDEAS_FRENTE,
    NEW_IDEAS_FONDO,
    HUERTA,
    HUERTA_LOCATION_IDEAS,
    DEFAULT_CONTACTS,
)
from styles import CSS
from scripts import JS

ROOT = Path(__file__).parent
IMAGES_DIR = ROOT / "images"
OUTPUT = ROOT / "docs" / "index.html"
TASKS_DIR = ROOT / "docs" / "tasks"
OG_DIR = ROOT / "docs" / "og"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
TASKS_DIR.mkdir(parents=True, exist_ok=True)
OG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# CONFIGURACIÓN — editar antes del primer deploy
# ============================================================
# URL pública de tu GitHub Pages.
# Ejemplo: "https://juan.github.io/jardineando-pacha-mama"
# Si está vacío, los previews de WhatsApp no van a funcionar (links rotos).
SITE_URL = "https://YOUR-USERNAME.github.io/jardineando-pacha-mama"


# ============================================================
# Helpers
# ============================================================
def encode_image(path: Path, max_width: int = 800, quality: int = 78) -> str:
    img = Image.open(path).convert("RGB")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"


def esc(s):
    return html_mod.escape(str(s) if s is not None else "", quote=True)


MONTH_NAMES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MONTH_FULL = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

TAG_STYLE = {
    "nativa": ("🇺🇾 nativa", "#4a6b3f"),
    "exotica": ("🌍 exótica", "#7a8c5c"),
    "frutal": ("🍑 frutal", "#d97706"),
    "aromatica": ("🌿 aromática", "#16a34a"),
    "ornamental": ("✨ ornamental", "#ca8a04"),
    "polinizadores": ("🐝 polinizadores", "#facc15"),
    "abejas": ("🐝 abejas", "#facc15"),
    "mariposas": ("🦋 mariposas", "#a855f7"),
    "picaflor": ("🐦 picaflor", "#ec4899"),
    "aves": ("🐦 aves", "#ec4899"),
    "trepadora": ("🌿 trepadora", "#0d9488"),
    "perfume": ("👃 perfume", "#e11d48"),
    "cerco-vivo": ("🌳 cerco-vivo", "#65a30d"),
    "comestible": ("🥬 comestible", "#16a34a"),
    "maceta": ("🪴 maceta", "#a16207"),
    "interior": ("🏠 interior", "#0284c7"),
    "purificadora": ("💨 purificadora", "#0284c7"),
    "sombra": ("🌑 sombra", "#475569"),
    "epifita": ("🌿 epífita", "#0d9488"),
    "rusticidad": ("💪 rústica", "#78716c"),
    "huerta": ("🥬 huerta", "#16a34a"),
    "fruto": ("🍅 fruto", "#dc2626"),
    "hoja": ("🥬 hoja", "#16a34a"),
    "raiz": ("🥕 raíz", "#f97316"),
    "bulbo": ("🧅 bulbo", "#a16207"),
    "verano": ("☀️ verano", "#eab308"),
    "invierno": ("❄️ invierno", "#0284c7"),
    "todo-año": ("🔄 todo el año", "#0d9488"),
    "rapida": ("⚡ rápida", "#facc15"),
    "perenne": ("♾️ perenne", "#4a6b3f"),
    "pendiente": ("⏳ pendiente", "#9333ea"),
    "fruta": ("🍓 fruta", "#dc2626"),
}

PRIORITY_STYLE = {
    "alta": ("🔴", "#dc2626", "Alta"),
    "media": ("🟡", "#ca8a04", "Media"),
    "baja": ("🟢", "#16a34a", "Baja"),
}


def render_tags(tags):
    return "".join(
        f'<span class="tag" style="background: {TAG_STYLE.get(t, ("", "#6b6457"))[1]}">{TAG_STYLE.get(t, (t,))[0]}</span>'
        for t in tags if t in TAG_STYLE
    )


def water_dots(water_str):
    if not water_str: return ""
    s = water_str.lower()
    if "muy bajo" in s or "tolera sequía" in s: return "💧"
    if "medio-bajo" in s: return "💧💧"
    if "medio-alto" in s: return "💧💧💧"
    if "bajo" in s: return "💧💧"
    if "alto" in s: return "💧💧💧💧"
    if "medio" in s: return "💧💧💧"
    return "💧"


def light_icon(light_str):
    if not light_str: return ""
    s = light_str.lower()
    if "pleno sol" in s or "sol pleno" in s: return "☀️☀️"
    if "sol parcial" in s or "sol o sombra" in s: return "🌤️"
    if "sombra parcial" in s: return "⛅"
    if "sombra" in s: return "🌑"
    if "sol" in s: return "☀️"
    return ""


# ============================================================
# Generación de tareas para Timeline
# ============================================================

# Mapeo: id_code (primer código) → "por qué hacer esta tarea"
# Justificación botánica que aparece al expandir la tarjeta.
WHY_BY_PLANT_ID = {
    "F-2": "La bignonia florece en madera nueva del año. Sin poda fuerte de invierno (40-60%), las ramas viejas dominan y las nuevas — que son las que producen las flores rosas — quedan ahogadas. Una poda severa en junio-julio asegura una floración explosiva de noviembre a abril.",
    "F-4": "Los Prunus (ciruelos) podan en plena dormancia para evitar 'gomosis' (exudado de savia que los enferma). En junio están sin savia activa, entonces la herida cierra limpia. Además podando ahora se elimina madera vieja improductiva y se mantiene la silueta abierta para que la luz entre al centro.",
    "F-8": "Es una nativa charrúa (Aguaribay/Molle) que no está bien documentada en el catálogo todavía. Necesitamos una foto desde la calle con su número visible para tener la referencia geográfica completa del jardín y poder ubicarlo en el mapa mental del frente.",
    "B-2": "Sin floración no podemos identificar este arbusto con certeza. La forma de la flor, color, perfume y patrón de inflorescencia son los datos clave para distinguir entre los muchos 'jazmines' posibles (de leche, del país, etc).",
    "B-5a": "Las hortensias en macetas chicas sufren estrés hídrico crónico — necesitan grandes volúmenes de agua y raíces extensas. Restringidas amarillean las hojas y la floración cae drásticamente. Junio es ideal porque están dormantes y no sufren el trasplante.",
    "B-9": "El crespón florece EXCLUSIVAMENTE en madera del año. Sin poda fuerte (50-70%), las flores aparecen en las puntas de ramas largas y débiles, dando una floración pobre y caída. Cuanto más drástica la poda invernal, más espectacular la floración estival — el famoso 'crepe murder' es un mito.",
    "B-13": "Las clivias forman colonias densas, pero cuando los bulbos asoman fuera del sustrato significa que ya no hay espacio para más raíces. Esto reduce la floración del año siguiente. Junio es el momento ideal porque está post-floración y entrando en reposo invernal.",
    "B-14": "Por la silueta y la posición podría ser un lapacho rosa (Handroanthus) — pero solo la floración primaveral con sus flores rosa-violáceas confirma. Si lo es, sería una nativa muy valiosa para sumar al inventario del jardín.",
    "B-15": "Desde lejos es imposible identificar — puede ser hiedra, parra silvestre, jazmín del país o un arbusto trepador. Una foto cercana de hojas y tallo es suficiente para clasificar y decidir si conviene mantenerla, podarla o reemplazarla.",
    "B-18": "Como el crespón, la Rosa de Siria florece en madera nueva. Una poda severa en invierno (40-50%) produce ramas vigorosas en primavera que cargan flores grandes y abundantes desde diciembre a marzo. Sin podar, la planta se vuelve leñosa y florece poco.",
    "B-20": "Sin hojas ni flores en mayo no hay datos suficientes para identificar. La hoja recién brotada y el patrón de ramas tiernas suelen ser distintivos — en septiembre tendremos el material para foto. Mientras tanto, la planta solo necesita riego mínimo.",
    "B-27": "Tiene flores secas pero sin certeza de la especie. La floración fresca da color, forma y disposición exacta — datos imprescindibles para identificar correctamente y poder dar consejos de cuidado precisos.",
    "B-29": "La lantana es nativa pero se vuelve leñosa y poco florífera si no se rejuvenece. Cortar a 30cm del suelo en invierno la obliga a renovar todo el follaje y volver a florecer espectacularmente en madera nueva — atrayendo mariposas y picaflores en primavera-verano.",
    "B-30": "REGLA #1 de los frutales de hueso: la fruta se forma en madera del año anterior. Sin poda invernal el durazno NO fructifica bien — las ramas viejas se cargan poco y la fruta es pequeña, escasa y de mala calidad. Es la tarea más crítica del año para este árbol.",
    "B-32": "Sin hojas ni flores no hay datos para identificar. El brote primaveral revela hoja, color, patrón y vigor. Esperar a septiembre permite una identificación precisa antes de tomar decisiones sobre poda o cuidados específicos.",
    "B-34": "La foto actual es panorámica y no permite ver detalles. Un closeup de hojas, tallo y flores (si las hay) basta para identificar. Sin esto no se pueden dar tips de poda o cuidados específicos.",
    "B-38": "Igual que el durazno — es un Prunus de hueso. Florece en agosto y fructifica en madera vieja del año anterior. La poda invernal renueva ramas y elimina las viejas que ya no producirán, permitiendo que la energía vaya a las nuevas que sí van a dar fruta.",
    "B-39": "Las peras necesitan poda invernal para mantener forma piramidal y eliminar 'chupones' (ramas verticales agresivas que no fructifican y le sacan energía al árbol). Sin podar, la planta se vuelve un caos de ramas y la fruta crece donde no llega luz, quedando pequeña y poco dulce.",
    "B-41": "Los caquis jóvenes necesitan poda de FORMACIÓN durante los primeros años para definir el tronco y las 3-4 ramas principales (estructura 'vaso'). Sin formación temprana, la planta puede tener una estructura débil que después es muy difícil de corregir y que no soporta bien el peso de los frutos.",
}


# Mapeo: id_code (primer código) → "cómo hacer la tarea bien" (instrucciones prácticas)
# Herramientas, técnica, época específica, qué evitar.
HOW_TO_DO_BY_PLANT_ID = {
    "F-2": (
        "**Cuándo:** día sin lluvia ni helada, esperá 3 días secos previos. Mañana mejor (sin sol fuerte).\n"
        "**Herramientas:** tijera de podar afilada + desinfectada con alcohol al 70%. Para ramas gruesas, serrucho de poda.\n"
        "**Pasos:** (1) Identificá las 3-4 ramas estructurales que querés conservar. (2) Cortá todas las guías largas a 30-40cm desde el origen. (3) Eliminá ramas cruzadas, secas o que se rozan. (4) Cada corte en bisel a 45°, 5mm sobre una yema externa.\n"
        "**Importante:** la bignonia rebrota fuerte — no tengas miedo de cortar mucho."
    ),
    "F-4": (
        "**Cuándo:** junio-julio cuando perdió todas las hojas. Día seco, frío, sin lluvia pronosticada 48h después.\n"
        "**Herramientas:** tijera afilada + serrucho para ramas gruesas. **DESINFECTAR con alcohol entre cada corte** (los Prunus son MUY sensibles a hongos).\n"
        "**Pasos:** (1) Eliminá ramas muertas, enfermas o rotas. (2) Eliminá chupones (verticales) y ramas que crecen al centro. (3) Acortá ramas principales 1/3 para mantener silueta abierta en V. (4) Cortes en bisel a 5mm de yema externa.\n"
        "**Crítico:** pintá los cortes mayores a 1.5cm con pasta cicatrizante — los Prunus pueden tomar gomosis por heridas abiertas."
    ),
    "F-8": (
        "**Cuándo:** día soleado entre 10-15h para mejor luz natural.\n"
        "**Posición:** parate en la calle, en la esquina opuesta del jardín, para encuadrar el árbol completo.\n"
        "**Pasos:** (1) Foto vertical mostrando el árbol entero. (2) Si podés, escribí el número 'F-8' en un cartón y ponelo cerca de la base. (3) Tomá 2-3 ángulos para tener opciones."
    ),
    "B-2": (
        "**Cuándo:** durante plena floración (5+ flores abiertas, primavera-verano).\n"
        "**Cámara/celular:** modo macro o acercate hasta enfocar.\n"
        "**Pasos:** (1) Closeup de UNA flor sola (a 1-2cm del lente). (2) Foto de toda la inflorescencia/racimo. (3) Foto de hoja por encima Y por debajo. (4) Anotá si tiene perfume y describilo (azahar, dulce, etc).\n"
        "**Hora ideal:** media mañana (10-11h), las flores están más abiertas."
    ),
    "B-5a": (
        "**Maceta nueva:** mínimo 40cm de diámetro × 40cm de profundidad. Mejor de barro o terracota (transpira).\n"
        "**Sustrato:** 60% tierra negra + 30% turba + 10% perlita. Las hortensias necesitan sustrato ácido (pH 5-6).\n"
        "**Pasos:** (1) Regá la planta 2h antes para que el cepellón se mantenga compacto. (2) Sacala con cuidado, no rompas el cepellón. (3) Si las raíces giran en espiral, rompelas levemente para que se expandan. (4) Centrala en maceta nueva al mismo nivel del suelo. (5) Riego abundante (que drene 2 veces). (6) Sombra durante 1 semana, después luz indirecta.\n"
        "**Tip:** para flores azules, agregá 5 clavos oxidados al fondo. Para rosa, una cucharada de cal."
    ),
    "B-9": (
        "**Cuándo:** junio-julio en plena dormancia (sin hojas).\n"
        "**Herramientas:** tijera grande + serrucho. Desinfectá con alcohol.\n"
        "**Pasos:** (1) Identificá 3-5 ramas principales para conservar. (2) Cortá el resto a 5-15cm de la base. (3) Las ramas conservadas: acortalas a la mitad o 1/3. (4) Cortes en bisel 45° hacia afuera de la yema.\n"
        "**No tengas miedo:** el crespón tolera podas drásticas y rebrota con flores enormes. La 'crepe murder' (poda al ras) es exagerada pero no mata el árbol."
    ),
    "B-13": (
        "**Maceta nueva:** apenas 5cm más de diámetro que la actual. Las clivias FLORECEN MEJOR cuando están un poco apretadas.\n"
        "**Sustrato:** mezcla para orquídeas + perlita + tierra común (proporciones 1:1:1).\n"
        "**Pasos:** (1) Sacá el cepellón entero. (2) Si tiene bulbos hijos, separalos con cuidado (cada uno será una nueva planta). (3) NO cortes raíces sanas — odian que se las toquen. (4) Plantá dejando 1/3 del bulbo expuesto al aire. (5) Regá moderadamente y esperá 2 semanas para volver a regar.\n"
        "**Ubicación:** sombra parcial, jamás sol directo de tarde."
    ),
    "B-14": (
        "**Cuándo:** primavera (septiembre-octubre) durante floración. Si es lapacho rosa, las flores aparecen ANTES que las hojas.\n"
        "**Pasos:** (1) Foto closeup de 1 flor entera. (2) Foto de la inflorescencia (racimo de flores). (3) Foto de la corteza del tronco (los lapachos tienen corteza distintiva). (4) Foto general del árbol completo desde lejos.\n"
        "**Pista:** si las flores son rosa-violáceas en racimos terminales, casi seguro es Handroanthus heptaphyllus (lapacho rosa)."
    ),
    "B-15": (
        "**Cuándo:** cualquier día con luz natural (no a mediodía con sol fuerte).\n"
        "**Pasos:** (1) Acercate hasta 30cm de la planta. (2) Foto de hojas — frente y dorso. (3) Foto del tallo principal mostrando textura. (4) Si tiene flores/frutos, closeup de esos. (5) Anotá: ¿trepa por el galpón o crece encima? ¿Tiene zarcillos? ¿Es leñosa o herbácea?"
    ),
    "B-18": (
        "**Cuándo:** junio-julio plena dormancia (sin hojas).\n"
        "**Herramientas:** tijera afilada y desinfectada con alcohol.\n"
        "**Pasos:** (1) Identificá 5-6 ramas principales sanas para conservar. (2) Cortá todas las demás a ras del suelo. (3) Las principales: cortalas a 30-50cm sobre el suelo. (4) Eliminá ramas que se cruzan o crecen al centro. (5) Cortes en bisel 45° hacia afuera de la yema.\n"
        "**Resultado esperado:** parecerá esqueleto pero rebrota con vigor en septiembre y florecerá fuerte en diciembre."
    ),
    "B-20": (
        "**Cuándo:** septiembre-octubre cuando empiece a brotar.\n"
        "**Pasos:** (1) Foto de hoja recién brotada (closeup). (2) Foto del patrón de ramificación general. (3) Si florece, foto de flor entera + closeup. (4) Anotá si las flores aparecen antes, después o junto con las hojas (dato clave para identificar)."
    ),
    "B-27": (
        "**Cuándo:** primavera durante floración fresca.\n"
        "**Pasos:** (1) Closeup de 1 flor sola. (2) Foto del racimo o conjunto de flores. (3) Foto general mostrando el porte colgante. (4) Anotá el color exacto (¿blanco, amarillo, lila?) y si tiene perfume."
    ),
    "B-29": (
        "**Cuándo:** junio-julio en invierno cuando casi no hay flores.\n"
        "**Equipo:** GUANTES (la lantana puede irritar la piel) + manga larga + tijera afilada.\n"
        "**Pasos:** (1) Cortá TODAS las ramas a 30cm del suelo. (2) No dejes ramas más gruesas de 1cm de diámetro. (3) Recogé TODOS los restos — incluidas bayas (que son tóxicas, especialmente para mascotas). (4) Regá bien después y aplicá mulch grueso.\n"
        "**Resultado:** parece destruida pero rebrota explosivamente en octubre, atrayendo mariposas y picaflores todo el verano."
    ),
    "B-30": (
        "**Cuándo:** JUNIO-JULIO en plena dormancia, sin hojas. Esta es la tarea más crítica del año para el durazno.\n"
        "**Herramientas:** tijera afilada + serrucho + alcohol al 70% para desinfectar **entre cada corte** (los Prunus son MUY sensibles a hongos como la monilia).\n"
        "**Pasos:** (1) Forma 'vaso abierto': dejá 3-4 ramas principales abiertas en V, eliminá el resto. (2) Eliminá 100% de los chupones (ramas verticales del centro). (3) Identificá las ramas que dieron fruta el año pasado (tienen cicatrices) y cortalas a 1/3. (4) Acortá ramas largas a 50cm. (5) Cortes en bisel 45°, 5mm sobre una yema externa.\n"
        "**CRÍTICO:** pintá TODOS los cortes de más de 1.5cm con pasta cicatrizante. Sin esto, el durazno puede contraer gomosis y morir en 2-3 años."
    ),
    "B-32": (
        "**Cuándo:** septiembre cuando empiezen a brotar.\n"
        "**Pasos:** (1) Foto de la primera hoja recién brotada. (2) Foto del patrón de ramas completo. (3) Si tiene flores tempranas, foto de esas también."
    ),
    "B-34": (
        "**Cuándo:** día con luz natural difusa (no sol directo a mediodía).\n"
        "**Pasos:** (1) Distancia 30-50cm de la planta. (2) Foto de hojas frente Y dorso. (3) Foto del tallo y patrón general. (4) Si hay flores o frutos, closeup. (5) Anotá tamaño aproximado de la planta."
    ),
    "B-38": (
        "**Cuándo:** junio-julio dormancia.\n"
        "**Herramientas:** tijera afilada + serrucho + alcohol para desinfectar entre cortes.\n"
        "**Pasos:** (1) Forma 'vaso abierto' como el durazno: 3-4 ramas principales. (2) Eliminá chupones verticales. (3) Acortá ramas que dieron fruto a 1/3. (4) Eliminá ramas más viejas que 4 años (las identificás por la corteza más oscura/agrietada).\n"
        "**Importante:** pintá cortes grandes con pasta cicatrizante (es Prunus, sensible a hongos)."
    ),
    "B-39": (
        "**Cuándo:** junio-julio dormancia.\n"
        "**Forma:** PIRAMIDAL (no vaso como Prunus): eje central + ramas en pisos horizontales.\n"
        "**Pasos:** (1) Mantené el eje central dominante. (2) Eliminá TODOS los chupones verticales — son ramas que no fructifican. (3) Acortá ramas largas a 1/3. (4) Eliminá ramas que se cruzan.\n"
        "**Ventaja:** no es necesario pintar cortes (los perales son menos sensibles a hongos que los Prunus)."
    ),
    "B-41": (
        "**Cuándo:** junio-julio dormancia.\n"
        "**Si es joven (< 4 años):** definí el tronco a 1m de altura y elegí 3-4 ramas principales bien distribuidas en distintas direcciones. Eliminá lo demás.\n"
        "**Si ya tiene estructura:** mantené la forma. Eliminá ramas que se cruzan o invaden el centro. Cortá 1/3 de las ramas más viejas (rebrota fácil en madera nueva).\n"
        "**Cortes:** en bisel sobre yema externa. No necesita pasta cicatrizante."
    ),
}


def generate_tasks_from_plants(plants):
    """
    Genera la lista canónica de tareas desde el catálogo de plantas.
    Cada planta con `urgency` produce 1 tarea.
    Si en el futuro queremos auto-derivar tareas estacionales (por ej. 'hay que regar'),
    se hace acá.
    """
    tasks = []
    for plant in plants:
        if not plant.get("urgency"):
            continue
        urg = plant["urgency"]
        # Sugerir contacto basado en tipo de acción
        action_lower = urg["action"].lower()
        if "poda" in action_lower or "trasplant" in action_lower:
            suggested_contact = "jardinero"
        elif "foto" in action_lower or "identificar" in action_lower:
            suggested_contact = None  # tarea propia
        else:
            suggested_contact = "jornalero"

        tasks.append({
            "id": f"plant-{plant['id_codes'][0]}",
            "kind": "plant_action",
            "plant_codes": plant["id_codes"],
            "plant_common": plant["common"],
            "plant_zone": plant["zone"],
            "plant_photo": plant.get("main_photo", ""),
            "title": urg["action"],
            "description": f"{plant['common']} ({', '.join(plant['id_codes'])}) — {urg['action']}.",
            "why": WHY_BY_PLANT_ID.get(plant['id_codes'][0], "Esta tarea aparece en el catálogo como pendiente. Marcala como hecha cuando la completes."),
            "how_to": HOW_TO_DO_BY_PLANT_ID.get(plant['id_codes'][0], ""),
            "priority": urg["priority"],
            "due_label": urg["when"],
            "due_month": urg.get("due_month"),
            "due_year": urg.get("due_year"),
            "suggested_contact": suggested_contact,
        })

    # Ordenar por prioridad y luego por fecha
    prio_order = {"alta": 0, "media": 1, "baja": 2}
    tasks.sort(key=lambda t: (
        prio_order.get(t["priority"], 3),
        t.get("due_year") or 9999,
        t.get("due_month") or 13,
    ))
    return tasks


# ============================================================
# Renderers — Plant cards (zone view)
# ============================================================
def render_plant_info_card(p, img_data):
    loc_codes = ", ".join(p["id_codes"])
    has_main = bool(p.get("main_photo") and img_data.get(p.get("main_photo")))
    has_loc = bool(p.get("loc_photo") and img_data.get(p.get("loc_photo")))

    photo_html = f'<img class="card-photo" data-img="{esc(p["main_photo"])}" data-action="lightbox" alt="">' if has_main else ''
    locs_html = f'<img class="card-loc-photo" data-img="{esc(p["loc_photo"])}" data-action="lightbox" alt="" title="Ver ubicación">' if has_loc else ''
    type_badge = {"caduco": "🍂 Caduco", "perenne": "🌲 Perenne", "semi-perenne": "🍃 Semi-perenne", "semi-caduco": "🍃 Semi-caduco"}.get(p.get("type", ""), p.get("type", ""))
    charrua_html = f'<div class="card-charrua">🪶 <strong>Originario:</strong> {esc(p["charrua"])}</div>' if p.get("charrua") else ''
    funfact_html = f'<div class="card-funfact">💡 <em>{esc(p["fun_fact"])}</em></div>' if p.get("fun_fact") and p["fun_fact"] != "—" else ''
    other_names_html = f'<div class="card-other">↳ {esc(p["other_names"])}</div>' if p.get("other_names") and p["other_names"] != "—" else ''

    return f"""
<article class="plant-card" data-plant-id="{esc(loc_codes)}" data-name="{esc(p['common'].lower())}" data-tags="{esc(' '.join(p['tags']))}">
  <div class="card-photo-wrap">
    {photo_html}
    <div class="card-loc-overlay">{locs_html}</div>
    <div class="card-id-pill">{esc(loc_codes)}</div>
  </div>
  <div class="card-body">
    <h3 class="card-title">{esc(p['common'])}</h3>
    <div class="card-sci">{esc(p['sci'])}</div>
    {charrua_html}
    {other_names_html}
    <div class="card-tags">{render_tags(p['tags'])}</div>
    <div class="card-type">{type_badge}</div>
    <p class="card-desc">{esc(p['desc'])}</p>
    {funfact_html}
  </div>
</article>"""


def render_plant_care_card(p):
    loc_codes = ", ".join(p["id_codes"])
    pruning_months = "".join(
        f'<span class="month-pill {"active" if m in p.get("pruning", []) else ""}">{MONTH_NAMES[m]}</span>'
        for m in range(1, 13)
    )
    urgency_html = ""
    if p.get("urgency"):
        u = p["urgency"]
        emo, color, label = PRIORITY_STYLE.get(u["priority"], ("", "#6b6457", u["priority"]))
        urgency_html = f"""
<div class="urgency-banner" style="border-left-color: {color}">
  <span class="urgency-badge" style="background: {color}">{emo} {label}</span>
  <strong>{esc(u["action"])}</strong>
  <span class="urgency-when">📅 {esc(u["when"])}</span>
</div>"""

    return f"""
<article class="care-card" data-plant-id="{esc(loc_codes)}" data-name="{esc(p['common'].lower())}">
  <div class="care-header">
    <div class="care-id">{esc(loc_codes)}</div>
    <h3 class="care-title">{esc(p['common'])}</h3>
    <div class="care-sci">{esc(p['sci'])}</div>
  </div>
  {urgency_html}
  <div class="care-grid">
    <div class="care-section">
      <div class="care-label">✂️ Cuándo podar</div>
      <div class="care-value">{esc(p['prune_when'])}</div>
      <div class="month-row">{pruning_months}</div>
    </div>
    <div class="care-section">
      <div class="care-label">📏 Cuánto podar</div>
      <div class="care-value">{esc(p['prune_how'])}</div>
    </div>
    <div class="care-section">
      <div class="care-label">💧 Riego <span class="big-icons">{water_dots(p['water'])}</span></div>
      <div class="care-value">{esc(p['water'])}</div>
    </div>
    <div class="care-section">
      <div class="care-label">{light_icon(p['light'])} Luz</div>
      <div class="care-value">{esc(p['light'])}</div>
    </div>
  </div>
</article>"""


def render_idea_card(idea):
    season = f'<div class="idea-season">📅 <strong>Plantar:</strong> {esc(idea["season_plant"])}</div>' if "season_plant" in idea else ''
    where = f'<div class="idea-where">📍 <strong>Dónde:</strong> {esc(idea["where"])}</div>' if "where" in idea else ''
    size = f'<div class="idea-size">📐 <strong>Tamaño:</strong> {esc(idea["size"])}</div>' if "size" in idea else ''

    return f"""
<article class="idea-card" data-name="{esc(idea['common'].lower())}" data-tags="{esc(' '.join(idea.get('tags', [])))}">
  <h3 class="idea-title">{esc(idea['common'])}</h3>
  <div class="idea-sci">{esc(idea.get('sci', ''))}</div>
  <div class="idea-type">{esc(idea['type'])}</div>
  <div class="idea-tags">{render_tags(idea.get('tags', []))}</div>
  <div class="idea-why"><strong>💚 Por qué:</strong> {esc(idea.get('why', ''))}</div>
  {where}
  {size}
  {season}
</article>"""


def render_huerta_card(h):
    def month_bar(months, color, label):
        bars = "".join(
            f'<div class="hcell {"active" if m in months else ""}" style="--c:{color}" title="{MONTH_FULL[m]}">{MONTH_NAMES[m]}</div>'
            for m in range(1, 13)
        )
        return f'<div class="hbar"><div class="hbar-label">{label}</div><div class="hbar-cells">{bars}</div></div>'

    cal_html = ""
    if h.get("siembra"): cal_html += month_bar(h["siembra"], "#16a34a", "🌱 Siembra")
    if h.get("transplante"): cal_html += month_bar(h["transplante"], "#0d9488", "🪴 Trasplante")
    if h.get("cosecha"): cal_html += month_bar(h["cosecha"], "#d97706", "🧺 Cosecha")

    return f"""
<article class="huerta-card" data-name="{esc(h['common'].lower())}" data-tags="{esc(' '.join(h.get('tags', [])))}">
  <div class="huerta-header">
    <h3 class="huerta-title">{esc(h['common'])}</h3>
    <div class="huerta-sci">{esc(h.get('sci', ''))}</div>
    <div class="huerta-type">{esc(h['type'])}</div>
  </div>
  <div class="huerta-tags">{render_tags(h.get('tags', []))}</div>
  <div class="huerta-tip"><strong>💡 Tip:</strong> {esc(h['tip'])}</div>
  <div class="huerta-meta">
    <span>{light_icon(h.get('sun', ''))} {esc(h.get('sun', ''))}</span>
    <span>{water_dots(h.get('water', ''))} {esc(h.get('water', ''))}</span>
  </div>
  <div class="hcal">{cal_html}</div>
</article>"""


def render_calendar_grid(plants_in_view):
    plants_zone = [p for p in plants_in_view if any([p.get("flowering"), p.get("fruiting"), p.get("pruning")])]
    plants_zone.sort(key=lambda p: p["common"])

    rows = []
    for p in plants_zone:
        cells = ""
        for m in range(1, 13):
            classes = []
            if m in p.get("flowering", []): classes.append("flor")
            if m in p.get("fruiting", []): classes.append("fruta")
            if m in p.get("pruning", []): classes.append("poda")
            cls = " ".join(classes) if classes else ""
            content = ""
            if "flor" in classes: content += '<span class="cal-emo">🌸</span>'
            if "fruta" in classes: content += '<span class="cal-emo">🍑</span>'
            if "poda" in classes: content += '<span class="cal-emo">✂️</span>'
            cells += f'<td class="cal-cell {cls}" title="{MONTH_FULL[m]}">{content}</td>'
        rows.append(f'<tr><td class="cal-name">{esc(p["common"])}<br><span class="cal-codes">{esc(", ".join(p["id_codes"]))}</span></td>{cells}</tr>')

    header_cells = "".join(f'<th class="cal-month">{MONTH_NAMES[m]}</th>' for m in range(1, 13))
    return f"""
<div class="cal-legend">
  <span class="leg-flor">🌸 Floración</span>
  <span class="leg-fruta">🍑 Fruta/cosecha</span>
  <span class="leg-poda">✂️ Poda</span>
</div>
<div class="cal-wrap">
  <table class="cal-table">
    <thead><tr><th class="cal-name-h">Planta</th>{header_cells}</tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</div>"""


def render_huerta_locations():
    cards = "".join(f"""
<article class="hloc-card">
  <h4 class="hloc-title">{esc(idea["title"])}</h4>
  <p class="hloc-desc">{esc(idea["desc"])}</p>
  <div class="hloc-pros"><strong>✅ Pros:</strong> {esc(idea["pros"])}</div>
  <div class="hloc-cons"><strong>⚠️ Contras:</strong> {esc(idea["cons"])}</div>
  <div class="hloc-best"><strong>👍 Mejor para:</strong> {esc(idea["best_for"])}</div>
</article>""" for idea in HUERTA_LOCATION_IDEAS)
    return f"""
<div class="hloc-intro">
  <h3>🤔 Aún no decidiste el espacio — acá te dejo opciones:</h3>
  <p>Ordenadas según mi recomendación (de mejor a más simple).</p>
</div>
<div class="hloc-grid">{cards}</div>
<h3 class="huerta-list-title">📋 Catálogo de cultivos para Uruguay</h3>
<p class="huerta-list-intro">Estos son los más recomendados para tu clima (Montevideo) y tu nivel de mantenimiento medio. Calendario marcado en meses.</p>
"""


# ============================================================
# Build de cada zona (Todo / Frente / Fondo)
# ============================================================
def build_zone(zone_name, zone_label, plants_in_view, ideas_list, show_huerta_locations, img_data):
    """
    plants_in_view: lista de plantas a mostrar (frente, fondo, o todas).
    ideas_list: lista de ideas nuevas a mostrar (puede ser combinación frente+fondo).
    show_huerta_locations: si True, muestra el intro con opciones de espacios para huerta
        (más apropiado para "fondo" y "todo"). Si False, muestra el intro corto del frente.
    """
    info_cards = "\n".join(render_plant_info_card(p, img_data) for p in plants_in_view)
    care_cards = "\n".join(render_plant_care_card(p) for p in plants_in_view)
    new_ideas = "\n".join(render_idea_card(i) for i in ideas_list)
    huerta_cards = "\n".join(render_huerta_card(h) for h in HUERTA)
    huerta_intro = render_huerta_locations() if show_huerta_locations else """
<div class="frente-huerta-intro">
  <h3>🌿 Aromáticas para el frente</h3>
  <p>El frente no es ideal para huerta clásica (visibilidad, espacio limitado). Pero podés sumar aromáticas y comestibles ornamentales que decoran y se cosechan.</p>
</div>"""
    cal_grid = render_calendar_grid(plants_in_view)

    return f"""
<section class="zone-content" data-zone="{zone_name}">
  <nav class="subtab-nav">
    <button class="subtab-btn active" data-sub="info">🪴 Nombres e info</button>
    <button class="subtab-btn" data-sub="care">✂️ Podas y cuidado</button>
    <button class="subtab-btn" data-sub="new">💡 Ideas nuevas</button>
    <button class="subtab-btn" data-sub="huerta">🥬 Ideas de huerta</button>
    <button class="subtab-btn" data-sub="cal">📅 Calendario</button>
  </nav>

  <div class="subtab-pane active" data-sub="info">
    <div class="filter-bar">
      <input type="text" class="search" placeholder="🔍 Buscar planta...">
      <div class="filter-tags" data-zone="{zone_name}">
        <button class="ftag active" data-filter="all">Todas</button>
        <button class="ftag" data-filter="nativa">🇺🇾 Nativas</button>
        <button class="ftag" data-filter="frutal">🍑 Frutales</button>
        <button class="ftag" data-filter="aromatica">🌿 Aromáticas</button>
        <button class="ftag" data-filter="ornamental">✨ Ornamentales</button>
        <button class="ftag" data-filter="trepadora">🌿 Trepadoras</button>
        <button class="ftag" data-filter="polinizadores">🐝 Polinizadores</button>
        <button class="ftag" data-filter="pendiente">⏳ Pendientes</button>
      </div>
    </div>
    <div class="cards-grid">{info_cards}</div>
  </div>

  <div class="subtab-pane" data-sub="care">
    <div class="filter-bar"><input type="text" class="search" placeholder="🔍 Buscar planta..."></div>
    <div class="cards-grid care-grid-list">{care_cards}</div>
  </div>

  <div class="subtab-pane" data-sub="new">
    <div class="ideas-intro">
      <h3>💡 Plantas recomendadas para sumar al {zone_label.lower()}</h3>
      <p>Basado en tu jardín actual, clima Montevideo y mantenimiento medio. Énfasis en nativas y polinizadores.</p>
    </div>
    <div class="cards-grid ideas-grid">{new_ideas}</div>
  </div>

  <div class="subtab-pane" data-sub="huerta">
    {huerta_intro}
    <div class="cards-grid huerta-grid">{huerta_cards}</div>
  </div>

  <div class="subtab-pane" data-sub="cal">
    <div class="ideas-intro">
      <h3>📅 Calendario anual de eventos del jardín</h3>
      <p>De un vistazo: cuándo florece cada planta, cuándo da fruto, y cuándo podarla.</p>
    </div>
    {cal_grid}
  </div>
</section>"""


# ============================================================
# Build TIMELINE view
# ============================================================
def build_timeline_view(tasks, img_data):
    """
    Renderiza la vista Timeline. La interactividad (estado, swipe, WhatsApp)
    está en scripts.py. Acá sólo serializamos los datos a JSON para que el JS
    los consuma.
    """
    # Pasamos sólo URLs de imagen referenciadas por tasks
    return """
<section class="zone-content" data-zone="timeline">
  <div class="timeline-header">
    <div class="timeline-intro">
      <h3>📋 Timeline de tareas</h3>
      <p>Tu próxima acción aparece arriba. Marcá hecho, posponé, o pedí ayuda con un mensaje pre-armado de WhatsApp.</p>
    </div>
    <div class="timeline-controls">
      <div class="filter-tags timeline-filters">
        <button class="ftag active" data-filter="active">📌 Activas</button>
        <button class="ftag" data-filter="done">✅ Hechas</button>
        <button class="ftag" data-filter="snoozed">😴 Pospuestas</button>
        <button class="ftag" data-filter="all">📚 Todas</button>
      </div>
      <button class="btn-contacts" id="btn-edit-contacts">📞 Mis contactos</button>
    </div>
  </div>

  <div class="timeline-summary" id="timeline-summary"></div>
  <div class="timeline-feed" id="timeline-feed"></div>
  <div class="timeline-empty" id="timeline-empty" style="display:none">
    <div class="empty-icon">🌿</div>
    <h3>Todo bajo control</h3>
    <p>No hay tareas en esta vista. ¡Podés volver más tarde!</p>
  </div>
</section>

<!-- Modal: Snooze -->
<div class="modal" id="snooze-modal">
  <div class="modal-content">
    <button class="modal-close" data-close="snooze">✕</button>
    <h3>😴 Posponer tarea</h3>
    <p class="snooze-task-name" id="snooze-task-name"></p>
    <div class="snooze-options">
      <button class="snooze-opt" data-days="1">⏰ Mañana</button>
      <button class="snooze-opt" data-days="3">📆 En 3 días</button>
      <button class="snooze-opt" data-days="7">🗓️ En 1 semana</button>
      <button class="snooze-opt" data-days="14">🗓️ En 2 semanas</button>
      <button class="snooze-opt" data-days="30">📅 En 1 mes</button>
      <button class="snooze-opt" data-days="90">📅 En 3 meses</button>
    </div>
    <div class="snooze-custom">
      <label>O elegí una fecha:</label>
      <input type="date" id="snooze-custom-date">
      <button class="btn-primary" id="btn-snooze-custom">Posponer hasta esta fecha</button>
    </div>
  </div>
</div>

<!-- Modal: WhatsApp -->
<div class="modal" id="whatsapp-modal">
  <div class="modal-content modal-wide">
    <button class="modal-close" data-close="whatsapp">✕</button>
    <h3>💬 Mensaje de WhatsApp</h3>
    <p class="whatsapp-task-name" id="whatsapp-task-name"></p>

    <div class="whatsapp-section">
      <label class="whatsapp-label">¿A quién le escribo?</label>
      <div class="whatsapp-contacts" id="whatsapp-contacts"></div>
    </div>

    <div class="whatsapp-section">
      <label class="whatsapp-label">Mensaje (editable):</label>
      <textarea class="whatsapp-message" id="whatsapp-message" rows="6" placeholder="Elegí un contacto arriba para ver el mensaje..."></textarea>
    </div>

    <div class="whatsapp-actions">
      <button class="btn-primary btn-wa" id="btn-send-whatsapp" disabled>
        💬 Abrir en WhatsApp
      </button>
    </div>
  </div>
</div>

<!-- Modal: Editar contactos -->
<div class="modal" id="contacts-modal">
  <div class="modal-content modal-wide">
    <button class="modal-close" data-close="contacts">✕</button>
    <h3>📞 Mis contactos</h3>
    <p class="contacts-intro">
      Editá teléfonos y plantilla por defecto. Se guarda solo en tu navegador (no se sube a internet).
    </p>
    <div id="contacts-list"></div>
    <div class="contacts-footer">
      <button class="btn-secondary" id="btn-reset-contacts">↺ Restaurar defaults</button>
      <button class="btn-primary" id="btn-save-contacts">💾 Guardar</button>
    </div>
  </div>
</div>"""


# ============================================================
# OG IMAGES + TASK PAGES (para WhatsApp / Facebook previews)
# ============================================================
def build_og_image(src_path: Path, dst_path: Path):
    """
    Genera una imagen 1200x630 (estándar Open Graph) con la foto de la tarea
    centrada y recortada estilo 'cover'.
    """
    target_w, target_h = 1200, 630
    img = Image.open(src_path).convert("RGB")

    # Resize escalando para "cover" (la imagen llena todo el target)
    src_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        # imagen más ancha — escalar por altura, recortar lados
        new_h = target_h
        new_w = int(target_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(target_w / src_ratio)

    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Crop centrado
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    img.save(dst_path, "JPEG", quality=82, optimize=True)


def build_task_page(task: dict, plant: dict | None):
    """
    Genera docs/tasks/{taskId}.html con OG meta tags específicos para esa tarea.
    Esta página al ser abierta en navegador redirige al index principal.
    Cuando se comparte el link por WhatsApp, los OG tags muestran el preview correcto.
    """
    task_id = task["id"]
    title = f"{task['title']} — {task['plant_common']}"

    # Description corta para OG (max ~200 chars)
    why = task.get("why") or task.get("description", "")
    if len(why) > 200:
        desc = why[:197].rsplit(" ", 1)[0] + "..."
    else:
        desc = why

    # OG image absoluta
    og_img_filename = f"{task_id}.jpg"
    og_image_url = f"{SITE_URL}/og/{og_img_filename}" if SITE_URL else ""
    page_url = f"{SITE_URL}/tasks/{task_id}.html" if SITE_URL else ""

    # Si no hay foto de planta, og_image queda vacío (no agregamos meta)
    has_og_image = task.get("plant_photo") and (IMAGES_DIR / task["plant_photo"]).exists()

    og_image_meta = ""
    if has_og_image and SITE_URL:
        og_image_meta = f"""
  <meta property="og:image" content="{esc(og_image_url)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(task['plant_common'])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{esc(og_image_url)}">"""

    page_url_meta = f'  <meta property="og:url" content="{esc(page_url)}">' if page_url else ""

    redirect_target = f"../index.html#task={task_id}"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{esc(title)} · Jardineando · Pacha Mama</title>
<meta name="description" content="{esc(desc)}">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Jardineando · Pacha Mama">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
{page_url_meta}
{og_image_meta}

<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">

<meta http-equiv="refresh" content="0; url={redirect_target}">
<link rel="canonical" href="{esc(page_url) if page_url else redirect_target}">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 40px; max-width: 600px; margin: 0 auto; text-align: center; color: #3f3f46; }}
  h1 {{ color: #15803d; font-size: 1.4rem; }}
  a {{ color: #2563eb; }}
</style>
</head>
<body>
<h1>🌿 Jardineando · Pacha Mama</h1>
<p>Redirigiendo a la tarea...</p>
<p><strong>{esc(title)}</strong></p>
<p><a href="{redirect_target}">Si no se redirige automáticamente, hacé click acá</a></p>
<script>window.location.replace("{redirect_target}");</script>
</body>
</html>"""

    out_path = TASKS_DIR / f"{task_id}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


# ============================================================
# Main
# ============================================================
def main():
    # 1. Cargar imágenes
    unique_files = set()
    for p in PLANTS:
        if p.get("loc_photo"): unique_files.add(p["loc_photo"])
        if p.get("main_photo"): unique_files.add(p["main_photo"])

    print(f"📷 Procesando {len(unique_files)} imágenes...")
    img_data = {}
    for fname in sorted(unique_files):
        path = IMAGES_DIR / fname
        if path.exists():
            img_data[fname] = encode_image(path)
        else:
            img_data[fname] = ""
            print(f"  ⚠ Faltante: {fname}")
    print(f"   ✅ {sum(1 for v in img_data.values() if v)} embebidas")

    # 2. Generar tareas
    tasks = generate_tasks_from_plants(PLANTS)
    print(f"📋 Tareas generadas: {len(tasks)}")

    # 2.5 Generar páginas OG por tarea + imágenes OG (1200x630)
    if SITE_URL and "YOUR-USERNAME" not in SITE_URL:
        og_count = 0
        page_count = 0
        plant_by_first_id = {p["id_codes"][0]: p for p in PLANTS}
        for task in tasks:
            plant = plant_by_first_id.get(task["plant_codes"][0])
            # Imagen OG si hay foto disponible
            if task.get("plant_photo"):
                src = IMAGES_DIR / task["plant_photo"]
                if src.exists():
                    dst = OG_DIR / f"{task['id']}.jpg"
                    build_og_image(src, dst)
                    og_count += 1
            build_task_page(task, plant)
            page_count += 1
        print(f"🔗 Páginas OG generadas: {page_count} (con imagen: {og_count})")
    else:
        print("⚠️  SITE_URL no configurado — páginas OG no generadas.")
        print("   Editá build.py y poné tu URL de GitHub Pages para activarlas.")

    # 3. Stats
    total_plants = len(PLANTS)
    total_native = sum(1 for p in PLANTS if "nativa" in p["tags"])
    total_frutal = sum(1 for p in PLANTS if "frutal" in p["tags"])
    total_urgent = sum(1 for p in PLANTS if p.get("urgency"))

    # 4. Build zonas
    frente_plants = [p for p in PLANTS if p["zone"] == "frente"]
    fondo_plants = [p for p in PLANTS if p["zone"] == "fondo"]

    todo_html = build_zone(
        "todo", "Todo el jardín", PLANTS,
        ideas_list=NEW_IDEAS_FRENTE + NEW_IDEAS_FONDO,
        show_huerta_locations=True, img_data=img_data,
    )
    frente_html = build_zone(
        "frente", "Frente", frente_plants,
        ideas_list=NEW_IDEAS_FRENTE,
        show_huerta_locations=False, img_data=img_data,
    )
    fondo_html = build_zone(
        "fondo", "Fondo", fondo_plants,
        ideas_list=NEW_IDEAS_FONDO,
        show_huerta_locations=True, img_data=img_data,
    )
    timeline_html = build_timeline_view(tasks, img_data)

    # 5. Inyectar datos como JSON para el JS
    img_js = "const IMG = " + json.dumps(img_data) + ";"
    tasks_js = "const TASKS = " + json.dumps(tasks, ensure_ascii=False) + ";"
    contacts_js = "const DEFAULT_CONTACTS = " + json.dumps(DEFAULT_CONTACTS, ensure_ascii=False) + ";"
    site_url_js = "const SITE_URL = " + json.dumps(SITE_URL if SITE_URL and "YOUR-USERNAME" not in SITE_URL else "") + ";"

    # 6. HTML final
    html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jardineando · Pacha Mama</title>
<style>{CSS}</style>
</head>
<body class="zone-todo">
<div class="container">
  <header class="main-header">
    <h1 class="brand"><span class="brand-emoji">🌿</span> Jardineando</h1>
    <h2 class="subbrand">Pacha Mama</h2>
    <div class="weather-line" id="weather-line">
      <span class="weather-emoji">🌱</span>
      <span class="weather-text">Consultando clima en Montevideo…</span>
    </div>
  </header>

  <div class="stats-strip">
    <span class="stat-chip"><span class="chip-icon">🌱</span><strong>{total_plants}</strong> especies</span>
    <span class="stat-chip"><span class="chip-icon">🇺🇾</span><strong>{total_native}</strong> nativas</span>
    <span class="stat-chip"><span class="chip-icon">🍑</span><strong>{total_frutal}</strong> frutales</span>
    <span class="stat-chip"><span class="chip-icon">🚨</span><strong>{total_urgent}</strong> pendientes</span>
  </div>
</div>

<nav class="main-tabs">
  <button class="tab-btn active" data-zone="todo"><span class="tab-emoji">🏡</span><span class="tab-label">Todo</span></button>
  <button class="tab-btn" data-zone="frente"><span class="tab-emoji">🌳</span><span class="tab-label">Frente</span></button>
  <button class="tab-btn" data-zone="fondo"><span class="tab-emoji">🏊</span><span class="tab-label">Fondo</span></button>
  <button class="tab-btn" data-zone="timeline"><span class="tab-emoji">📋</span><span class="tab-label">Timeline</span></button>
</nav>

<div class="container container-zones">
  {todo_html.replace('class="zone-content"', 'class="zone-content active"', 1)}
  {frente_html}
  {fondo_html}
  <div class="zone-content" data-zone="timeline">{timeline_html.split('<section class="zone-content" data-zone="timeline">', 1)[1].split('</section>', 1)[0]}</div>
  {timeline_html.split('</section>', 1)[1]}
</div>

<div class="lightbox" id="lightbox">
  <img id="lightbox-img" alt="">
</div>

<script>
{img_js}
{tasks_js}
{contacts_js}
{site_url_js}
{JS}
</script>
</body>
</html>"""

    OUTPUT.write_text(html_doc, encoding="utf-8")
    size_mb = OUTPUT.stat().st_size / 1024 / 1024
    print(f"\n✅ Generado: {OUTPUT}")
    print(f"   {size_mb:.1f} MB · {total_plants} plantas · {len(tasks)} tareas")
    print(f"\n👉 Para subir a GitHub Pages:")
    print(f"   git add docs/index.html && git commit -m 'rebuild' && git push")


if __name__ == "__main__":
    main()
