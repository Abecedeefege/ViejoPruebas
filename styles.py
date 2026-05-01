"""
Estilos CSS — diseño minimalista moderno.
Inter font · paleta neutra zinc + accent verde · bordes en lugar de sombras pesadas.
"""

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Surfaces */
  --bg: #fafafa;
  --bg-card: #ffffff;
  --bg-soft: #f4f4f5;
  --bg-hover: #f4f4f5;

  /* Text */
  --text: #09090b;
  --text-2: #3f3f46;
  --text-3: #71717a;
  --text-muted: #a1a1aa;

  /* Borders */
  --border: #e4e4e7;
  --border-soft: #f4f4f5;
  --border-strong: #d4d4d8;

  /* Accent (green) */
  --accent: #15803d;
  --accent-hover: #166534;
  --accent-soft: #f0fdf4;
  --accent-text: #14532d;

  /* States */
  --red: #dc2626;
  --red-soft: #fef2f2;
  --orange: #ea580c;
  --orange-soft: #fff7ed;
  --green: #16a34a;
  --green-soft: #f0fdf4;
  --blue: #2563eb;
  --blue-soft: #eff6ff;
  --whatsapp: #25d366;
  --whatsapp-hover: #1da851;

  /* Shadows — minimal */
  --shadow-xs: 0 1px 2px rgba(9, 9, 11, 0.04);
  --shadow-sm: 0 1px 3px rgba(9, 9, 11, 0.06), 0 1px 2px rgba(9, 9, 11, 0.04);
  --shadow-md: 0 4px 6px -1px rgba(9, 9, 11, 0.06), 0 2px 4px -2px rgba(9, 9, 11, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(9, 9, 11, 0.08), 0 4px 6px -4px rgba(9, 9, 11, 0.04);

  /* Radii */
  --r-sm: 6px;
  --r-md: 8px;
  --r-lg: 12px;
  --r-xl: 16px;
  --r-full: 999px;

  /* Transitions */
  --t: 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0; padding: 0;
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-feature-settings: 'cv11', 'ss01';
  letter-spacing: -0.011em;
  min-height: 100vh;
  transition: background-color 600ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Backgrounds pastel — sutiles pero notorios — uno por zona */
body.zone-todo    { background: #fafafa; }      /* zinc neutral */
body.zone-frente  { background: #fbf7ec; }      /* crema cálido — calle, sol */
body.zone-fondo   { background: #eff5fc; }      /* celeste agua — piscina */
body.zone-timeline{ background: #f1f7ec; }      /* verde menta — tareas */

button, input, textarea, select {
  font-family: inherit;
  font-size: inherit;
  letter-spacing: inherit;
}

.container { max-width: 1280px; margin: 0 auto; padding: 32px 24px 96px; }

/* HEADER */
header.main-header {
  text-align: left;
  padding: 24px 0 32px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 32px;
}
h1.brand {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  margin: 0 0 8px;
  color: var(--text);
}
.brand-emoji { display: none; }
h2.subbrand {
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 500;
  letter-spacing: -0.01em;
  color: var(--accent);
  margin: 0 0 16px;
  font-style: normal;
}
.weather-line {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  color: var(--text-3);
  margin: 0;
  padding: 6px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-full);
  font-weight: 500;
}
.weather-line .weather-emoji { font-size: 1.05rem; line-height: 1; }
.weather-line strong { color: var(--text); font-weight: 600; }
.weather-line .weather-sep { color: var(--text-muted); margin: 0 2px; }
/* STATS STRIP */
.stats-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 16px 0 0;
  padding: 0;
}
.stat-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-full);
  font-size: 0.78rem;
  color: var(--text-3);
  line-height: 1.4;
  white-space: nowrap;
}
.stat-chip strong {
  color: var(--text);
  font-weight: 600;
  font-feature-settings: 'tnum';
}
.stat-chip .chip-icon {
  font-size: 0.85rem;
  line-height: 1;
}

/* MAIN TABS — full width, sticky, cada tab a 25% */
.main-tabs {
  display: flex;
  gap: 0;
  margin: 0;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  flex-wrap: nowrap;
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.92);
}
.tab-btn {
  flex: 1 1 0;
  min-width: 0;
  background: transparent;
  border: none;
  padding: 14px 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 0;
  color: var(--text-3);
  transition: color var(--t), background var(--t);
  position: relative;
  border-bottom: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tab-btn:hover {
  color: var(--text);
  background: var(--bg-soft);
}
.tab-btn.active {
  color: var(--text);
  background: transparent;
  border-bottom-color: var(--text);
  font-weight: 600;
}
.tab-emoji { font-size: 1rem; line-height: 1; }
.tab-label { line-height: 1; }

/* container que envuelve las zonas — agrega padding top luego del nav sticky */
.container-zones {
  padding-top: 32px;
}

/* SUBTABS */
.subtab-nav {
  display: flex; gap: 4px; margin: 0 0 24px;
  padding: 4px; background: var(--bg-soft);
  border-radius: var(--r-md);
  border: 1px solid var(--border);
  flex-wrap: wrap; box-shadow: none;
}
.subtab-btn {
  background: transparent; border: none;
  padding: 8px 14px;
  font-size: 0.85rem; font-weight: 500;
  cursor: pointer; border-radius: var(--r-sm);
  color: var(--text-3);
  transition: all var(--t);
  flex: 0 1 auto; min-width: auto;
  white-space: nowrap;
}
.subtab-btn:hover { background: var(--bg-card); color: var(--text); }
.subtab-btn.active {
  background: var(--bg-card); color: var(--text);
  font-weight: 600; box-shadow: var(--shadow-xs);
}

/* PANES */
.zone-content { display: none; }
.zone-content.active { display: block; animation: fadeIn 0.25s ease; }
.subtab-pane { display: none; }
.subtab-pane.active { display: block; animation: fadeIn 0.25s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* FILTERS */
.filter-bar {
  display: flex; gap: 12px;
  margin-bottom: 24px; flex-wrap: wrap;
  align-items: center;
}
.search {
  flex: 1; min-width: 240px;
  padding: 10px 16px;
  font-size: 0.9rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  color: var(--text);
  transition: border-color var(--t), box-shadow var(--t);
}
.search::placeholder { color: var(--text-muted); }
.search:focus {
  outline: none; border-color: var(--text-2);
  box-shadow: 0 0 0 3px rgba(9, 9, 11, 0.04);
}
.filter-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.ftag {
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 6px 12px;
  font-size: 0.8rem; font-weight: 500;
  cursor: pointer; border-radius: var(--r-full);
  color: var(--text-2);
  transition: all var(--t);
}
.ftag:hover { background: var(--bg-soft); border-color: var(--border-strong); }
.ftag.active { background: var(--text); color: white; border-color: var(--text); }

/* CARDS GRID */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}
.cards-grid.care-grid-list { grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); }

/* PLANT INFO CARD */
.plant-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden; box-shadow: none;
  transition: border-color var(--t), transform var(--t), box-shadow var(--t);
  display: flex; flex-direction: column;
}
.plant-card:hover {
  border-color: var(--border-strong);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}
.card-photo-wrap {
  position: relative; width: 100%; height: 200px;
  overflow: hidden; background: var(--bg-soft);
}
.card-photo {
  width: 100%; height: 100%;
  object-fit: cover; cursor: zoom-in;
  transition: transform 0.4s ease;
}
.card-photo:hover { transform: scale(1.03); }
.card-loc-overlay {
  position: absolute; bottom: 12px; right: 12px;
  width: 52px; height: 52px;
  border-radius: var(--r-md);
  overflow: hidden;
  border: 2px solid var(--bg-card);
  box-shadow: var(--shadow-md);
  background: var(--bg-card);
}
.card-loc-photo { width: 100%; height: 100%; object-fit: cover; cursor: zoom-in; }
.card-id-pill {
  position: absolute; top: 12px; left: 12px;
  background: rgba(9, 9, 11, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: white; padding: 4px 10px;
  border-radius: var(--r-sm);
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.72rem; font-weight: 500;
}
.card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; }
.card-title {
  font-size: 1.05rem; font-weight: 600;
  margin: 0 0 2px; color: var(--text);
  line-height: 1.3; letter-spacing: -0.01em;
  font-family: inherit;
}
.card-sci {
  font-style: italic; color: var(--text-3);
  font-size: 0.82rem; margin-bottom: 12px;
  font-weight: 400;
}
.card-charrua {
  font-size: 0.78rem; color: var(--text-2);
  margin-bottom: 8px; background: var(--bg-soft);
  padding: 4px 8px; border-radius: var(--r-sm);
  display: inline-block; font-weight: 500;
}
.card-charrua strong { font-weight: 600; }
.card-other { font-size: 0.78rem; color: var(--text-3); margin-bottom: 8px; }
.card-tags { display: flex; flex-wrap: wrap; gap: 4px; margin: 8px 0 12px; }
.tag {
  font-size: 0.7rem; padding: 3px 8px;
  border-radius: var(--r-sm);
  color: white; white-space: nowrap;
  font-weight: 500;
}
.card-type {
  font-size: 0.78rem; color: var(--text-2);
  margin-bottom: 12px; padding: 3px 10px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  display: inline-block; font-weight: 500;
}
.card-desc {
  font-size: 0.88rem; line-height: 1.55;
  color: var(--text-2); margin: 8px 0 0; flex: 1;
}
.card-funfact {
  font-size: 0.82rem; color: var(--text-2);
  background: var(--accent-soft);
  border: 1px solid #dcfce7;
  padding: 10px 12px; margin-top: 12px;
  border-radius: var(--r-md);
  border-left: none; line-height: 1.5;
}
.card-funfact em { font-style: normal; color: var(--accent-text); }

/* CARE CARD */
.care-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden; box-shadow: none;
  display: flex; flex-direction: column;
}
.care-header {
  padding: 18px 20px 14px;
  background: var(--bg-card); color: var(--text);
  border-bottom: 1px solid var(--border);
}
.care-id {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.72rem; color: var(--text-3);
  margin-bottom: 4px; opacity: 1; font-weight: 500;
}
.care-title {
  font-family: inherit; margin: 0;
  font-size: 1.1rem; font-weight: 600;
  letter-spacing: -0.01em; line-height: 1.3;
}
.care-sci {
  font-style: italic; font-size: 0.82rem;
  color: var(--text-3); opacity: 1; margin-top: 2px;
}
.urgency-banner {
  background: var(--bg-soft);
  border-left: 3px solid;
  padding: 12px 16px;
  display: flex; flex-wrap: wrap;
  align-items: center; gap: 10px;
  font-size: 0.85rem;
}
.urgency-badge {
  color: white; padding: 2px 8px;
  border-radius: var(--r-sm);
  font-size: 0.7rem; font-weight: 600;
  white-space: nowrap; letter-spacing: 0.02em;
}
.urgency-when {
  margin-left: auto; color: var(--text-3);
  font-size: 0.8rem; font-weight: 500;
}
.care-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 0; background: var(--border-soft); padding: 1px;
}
.care-section { background: var(--bg-card); padding: 14px 16px; }
.care-label {
  font-size: 0.7rem; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--text-3);
  font-weight: 600; margin-bottom: 6px;
}
.big-icons { font-size: 0.85rem; margin-left: 4px; }
.care-value { font-size: 0.85rem; line-height: 1.5; color: var(--text); }
.month-row { display: flex; gap: 3px; margin-top: 10px; flex-wrap: wrap; }
.month-pill {
  font-size: 0.68rem; padding: 3px 7px;
  background: var(--bg-soft); color: var(--text-3);
  border-radius: var(--r-sm); font-weight: 500;
  text-transform: lowercase;
  border: 1px solid var(--border-soft);
}
.month-pill.active {
  background: var(--text); color: white;
  font-weight: 600; border-color: var(--text);
}

/* IDEA CARD */
.idea-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: var(--r-lg);
  padding: 20px; box-shadow: none;
  transition: all var(--t);
}
.idea-card:hover {
  border-color: var(--border-strong);
  border-left-color: var(--accent);
  box-shadow: var(--shadow-sm);
}
.idea-title {
  font-family: inherit; font-size: 1.05rem;
  font-weight: 600; margin: 0 0 2px;
  color: var(--text); letter-spacing: -0.01em;
}
.idea-sci { font-style: italic; color: var(--text-3); font-size: 0.82rem; margin-bottom: 8px; }
.idea-type {
  font-size: 0.78rem; background: var(--bg-soft);
  border: 1px solid var(--border);
  padding: 2px 10px; border-radius: var(--r-sm);
  display: inline-block; color: var(--text-2);
  margin-bottom: 10px; font-weight: 500;
}
.idea-tags { display: flex; flex-wrap: wrap; gap: 4px; margin: 8px 0 12px; }
.idea-why, .idea-where, .idea-size, .idea-season {
  font-size: 0.85rem; margin: 8px 0;
  color: var(--text-2); line-height: 1.5;
}
.idea-why { color: var(--text); margin-bottom: 12px; }
.idea-where {
  background: var(--bg-soft);
  padding: 10px 12px;
  border-radius: var(--r-md);
  border-left: none;
  border: 1px solid var(--border-soft);
}
.idea-season {
  background: var(--accent-soft);
  padding: 10px 12px;
  border-radius: var(--r-md);
  border-left: none;
  border: 1px solid #dcfce7;
  color: var(--accent-text);
}
.ideas-intro {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--text);
  padding: 18px 22px;
  margin-bottom: 28px;
  border-radius: var(--r-md);
}
.ideas-intro h3 {
  font-family: inherit; margin: 0 0 6px;
  color: var(--text); font-size: 1.05rem;
  font-weight: 600; letter-spacing: -0.01em;
}
.ideas-intro p { margin: 0; color: var(--text-3); font-size: 0.88rem; line-height: 1.55; }

/* HUERTA CARD */
.huerta-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-top: 3px solid var(--accent);
  border-radius: var(--r-lg);
  padding: 20px; box-shadow: none;
  transition: all var(--t);
}
.huerta-card:hover { box-shadow: var(--shadow-sm); }
.huerta-header { margin-bottom: 8px; }
.huerta-title {
  font-family: inherit; font-size: 1.05rem;
  font-weight: 600; margin: 0 0 2px;
  color: var(--text); letter-spacing: -0.01em;
}
.huerta-sci { font-style: italic; color: var(--text-3); font-size: 0.82rem; }
.huerta-type { font-size: 0.78rem; color: var(--text-3); margin-bottom: 8px; }
.huerta-tags { display: flex; gap: 4px; flex-wrap: wrap; margin: 8px 0; }
.huerta-tip {
  font-size: 0.85rem;
  background: var(--bg-soft);
  border: 1px solid var(--border-soft);
  padding: 10px 12px; border-radius: var(--r-md);
  margin: 12px 0; color: var(--text-2);
  line-height: 1.5;
}
.huerta-meta {
  display: flex; flex-wrap: wrap; gap: 16px;
  font-size: 0.8rem; color: var(--text-3);
  margin: 12px 0;
}
.hcal { margin-top: 14px; }
.hbar {
  display: grid; grid-template-columns: 100px 1fr;
  gap: 8px; margin-bottom: 4px; align-items: center;
}
.hbar-label { font-size: 0.72rem; font-weight: 500; color: var(--text-3); }
.hbar-cells { display: grid; grid-template-columns: repeat(12, 1fr); gap: 2px; }
.hcell {
  font-size: 0.62rem; text-align: center;
  padding: 4px 0; background: var(--bg-soft);
  color: var(--text-muted); border-radius: var(--r-sm);
  font-weight: 500; text-transform: lowercase;
}
.hcell.active { background: var(--c, var(--accent)); color: white; font-weight: 600; }

/* HUERTA LOCATIONS */
.hloc-intro { margin-bottom: 24px; }
.hloc-intro h3 {
  font-family: inherit; color: var(--text);
  margin: 0 0 6px; font-size: 1.1rem;
  font-weight: 600; letter-spacing: -0.01em;
}
.hloc-intro p { color: var(--text-3); margin: 0; font-size: 0.9rem; }
.hloc-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px; margin-bottom: 40px;
}
.hloc-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-top: 3px solid var(--text);
  border-radius: var(--r-lg);
  padding: 18px 20px; box-shadow: none;
  transition: all var(--t);
}
.hloc-card:hover { box-shadow: var(--shadow-sm); }
.hloc-title {
  font-family: inherit; font-size: 1rem;
  margin: 0 0 10px; color: var(--text);
  font-weight: 600; letter-spacing: -0.01em;
}
.hloc-desc { font-size: 0.85rem; margin-bottom: 12px; color: var(--text-2); line-height: 1.55; }
.hloc-pros, .hloc-cons, .hloc-best {
  font-size: 0.8rem; margin: 6px 0;
  padding: 8px 10px; border-radius: var(--r-md);
  line-height: 1.5;
}
.hloc-pros { background: var(--green-soft); color: var(--accent-text); }
.hloc-cons { background: var(--orange-soft); color: #9a3412; }
.hloc-best { background: var(--blue-soft); color: #1e40af; }
.huerta-list-title {
  font-family: inherit; color: var(--text);
  margin: 40px 0 6px; font-size: 1.5rem;
  font-weight: 700; letter-spacing: -0.02em;
  border-top: 1px solid var(--border);
  padding-top: 32px;
}
.huerta-list-intro {
  color: var(--text-3); font-style: normal;
  margin-bottom: 24px; font-size: 0.9rem;
}
.frente-huerta-intro {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--text);
  padding: 18px 22px;
  margin-bottom: 28px;
  border-radius: var(--r-md);
}
.frente-huerta-intro h3 {
  font-family: inherit; margin: 0 0 4px;
  color: var(--text); font-size: 1.05rem; font-weight: 600;
}
.frente-huerta-intro p { margin: 0; color: var(--text-3); font-size: 0.88rem; }

/* CALENDAR */
.cal-legend {
  display: flex; gap: 16px; flex-wrap: wrap;
  font-size: 0.85rem; margin-bottom: 16px;
  color: var(--text-3);
}
.cal-wrap {
  overflow-x: auto;
  background: var(--bg-card);
  border-radius: var(--r-lg);
  padding: 16px; box-shadow: none;
  border: 1px solid var(--border);
}
.cal-table {
  width: 100%; border-collapse: separate;
  border-spacing: 2px; min-width: 800px;
}
.cal-table th {
  font-family: inherit; font-size: 0.72rem;
  font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--text-3);
  padding: 6px 4px; text-align: center;
}
.cal-name-h { text-align: left !important; min-width: 180px; }
.cal-name {
  font-size: 0.85rem; font-weight: 500;
  padding: 8px 12px; background: var(--bg-soft);
  border-radius: var(--r-sm); white-space: nowrap;
  color: var(--text);
}
.cal-codes {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.68rem; color: var(--text-3); font-weight: 400;
}
.cal-cell {
  background: var(--bg-soft); border-radius: var(--r-sm);
  text-align: center; height: 32px; vertical-align: middle;
  font-size: 0.85rem; position: relative;
  transition: background var(--t);
}
.cal-cell.flor { background: #fce7f3; }
.cal-cell.fruta { background: #fed7aa; }
.cal-cell.poda { background: #e0e7ff; color: var(--text); }
.cal-cell.flor.fruta { background: #fbcfe8; }
.cal-cell.flor.poda { background: #fce7f3; }
.cal-cell.fruta.poda { background: #fed7aa; }
.cal-cell.flor.fruta.poda { background: #fed7aa; }

/* LIGHTBOX */
.lightbox {
  display: none; position: fixed; inset: 0;
  background: rgba(9, 9, 11, 0.95);
  z-index: 1000; align-items: center;
  justify-content: center; cursor: zoom-out; padding: 24px;
}
.lightbox.active { display: flex; }
.lightbox img {
  max-width: 95vw; max-height: 95vh;
  object-fit: contain; border-radius: var(--r-md);
}

/* TIMELINE */
.timeline-header {
  display: flex; flex-direction: column;
  gap: 20px; margin-bottom: 24px;
}
.timeline-intro {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--text);
  padding: 18px 22px; border-radius: var(--r-md);
}
.timeline-intro h3 {
  font-family: inherit; margin: 0 0 4px;
  color: var(--text); font-size: 1.1rem;
  font-weight: 600; letter-spacing: -0.01em;
}
.timeline-intro p { margin: 0; color: var(--text-3); font-size: 0.9rem; line-height: 1.55; }
.timeline-controls {
  display: flex; justify-content: space-between;
  flex-wrap: wrap; gap: 12px; align-items: center;
}
.btn-contacts {
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 8px 14px;
  font-size: 0.85rem; font-weight: 500;
  cursor: pointer; border-radius: var(--r-md);
  color: var(--text-2); transition: all var(--t);
}
.btn-contacts:hover {
  background: var(--text); color: white; border-color: var(--text);
}
.timeline-summary {
  background: var(--bg-card);
  border-radius: var(--r-lg);
  padding: 18px 24px; margin-bottom: 24px;
  box-shadow: none; display: flex;
  gap: 32px; flex-wrap: wrap;
  border: 1px solid var(--border);
}
.timeline-summary .stat-block { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
.timeline-summary .stat-num {
  font-size: 1.75rem; font-weight: 700;
  font-family: inherit; color: var(--text);
  line-height: 1; letter-spacing: -0.02em;
}
.timeline-summary .stat-label {
  font-size: 0.78rem; color: var(--text-3);
  font-weight: 500; text-transform: uppercase;
  letter-spacing: 0.05em;
}
.timeline-feed {
  display: flex; flex-direction: column;
  gap: 12px; max-width: 720px; margin: 0 auto;
}
.timeline-empty {
  text-align: center; padding: 80px 24px;
  background: var(--bg-card);
  border-radius: var(--r-lg);
  margin: 24px auto; max-width: 500px;
  border: 1px solid var(--border);
}
.timeline-empty .empty-icon { font-size: 3rem; margin-bottom: 12px; opacity: 0.5; }
.timeline-empty h3 {
  font-family: inherit; color: var(--text);
  margin: 0 0 6px; font-size: 1.15rem; font-weight: 600;
}
.timeline-empty p { color: var(--text-3); margin: 0; font-size: 0.9rem; }

/* TASK CARD */
.task-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--text-muted);
  border-radius: var(--r-lg);
  overflow: hidden; box-shadow: none;
  position: relative;
  transition: border-color var(--t), box-shadow var(--t);
  touch-action: pan-y;
  display: flex;
  align-items: stretch;
}
.task-card:hover { border-color: var(--border-strong); box-shadow: var(--shadow-sm); }
.task-card.swiping { transition: none; }
.task-card.swipe-out-right {
  transform: translateX(120%) rotate(6deg);
  opacity: 0; transition: transform 0.35s, opacity 0.35s;
}
.task-card.swipe-out-left {
  transform: translateX(-120%) rotate(-6deg);
  opacity: 0; transition: transform 0.35s, opacity 0.35s;
}
.task-card.priority-alta { border-left-color: var(--red); }
.task-card.priority-media { border-left-color: var(--orange); }
.task-card.priority-baja { border-left-color: var(--green); }
.task-card.completed { opacity: 0.6; background: var(--bg-soft); }
.task-card.snoozed { opacity: 0.85; background: var(--bg); }

/* Contenido principal flex 1 */
.task-content-wrap {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

/* Side hints — indicadores fijos a izquierda/derecha que sugieren swipe */
.task-side-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0 14px;
  background: var(--bg-soft);
  color: var(--text-3);
  user-select: none;
  pointer-events: none;
  white-space: nowrap;
  flex-shrink: 0;
  opacity: 0.7;
  transition: opacity 0.15s, color 0.15s, background 0.15s;
}
.task-side-hint.left { border-right: 1px solid var(--border-soft); }
.task-side-hint.right { border-left: 1px solid var(--border-soft); }
.task-side-hint.right .hint-icon { color: var(--whatsapp); }
.task-side-hint.right .hint-icon svg { fill: var(--whatsapp); }
.task-side-hint .hint-arrow {
  font-size: 1.4rem;
  font-weight: 600;
  line-height: 1;
}
.task-side-hint .hint-icon {
  font-size: 1.05rem;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.task-side-hint .hint-icon svg {
  width: 18px;
  height: 18px;
  display: block;
}

/* Brillan cuando arrastrás en su dirección */
.task-card[data-dx-negative="true"] .task-side-hint.left {
  opacity: 1;
  color: var(--text);
  background: var(--bg-elevated, var(--bg-soft));
}
.task-card[data-dx-positive="true"] .task-side-hint.right {
  opacity: 1;
  color: var(--whatsapp);
  background: rgba(37, 211, 102, 0.12);
}

.task-header {
  display: flex; gap: 14px;
  padding: 16px; align-items: flex-start;
  cursor: pointer;
  user-select: none;
}
.task-card.completed .task-header,
.task-card.snoozed .task-header { cursor: pointer; }
.task-photo {
  width: 72px; height: 72px;
  object-fit: cover; border-radius: var(--r-md);
  flex-shrink: 0; background: var(--bg-soft); cursor: zoom-in;
}
.task-photo-placeholder {
  width: 72px; height: 72px;
  background: var(--bg-soft);
  border-radius: var(--r-md);
  flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem;
  border: 1px solid var(--border-soft);
}
.task-meta { flex: 1; min-width: 0; }
.task-meta-top {
  display: flex; align-items: center; gap: 6px;
  flex-wrap: wrap; margin-bottom: 6px;
}
.task-priority-pill {
  color: white; padding: 2px 8px;
  border-radius: var(--r-sm);
  font-size: 0.68rem; font-weight: 600;
  white-space: nowrap; letter-spacing: 0.02em;
  text-transform: uppercase;
}
.task-zone-pill {
  background: var(--bg-soft); color: var(--text-3);
  padding: 2px 8px; border-radius: var(--r-sm);
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  border: 1px solid var(--border-soft); font-weight: 500;
}
.task-status-pill {
  padding: 2px 8px; border-radius: var(--r-sm);
  font-size: 0.7rem; font-weight: 500;
}
.task-status-pill.done {
  background: var(--green-soft); color: var(--accent-text);
  border: 1px solid #bbf7d0;
}
.task-status-pill.snoozed {
  background: var(--bg-soft); color: var(--text-3);
  border: 1px solid var(--border);
}
.task-expand-chevron {
  margin-left: auto;
  font-size: 0.95rem;
  color: var(--text-muted);
  transition: transform 0.25s ease, color var(--t);
  user-select: none;
  line-height: 1;
}
.task-card:hover .task-expand-chevron { color: var(--text-3); }
.task-card.expanded .task-expand-chevron {
  transform: rotate(180deg);
  color: var(--text);
}
.task-header {
  display: flex; gap: 14px;
  padding: 16px; align-items: flex-start;
  cursor: pointer;
  user-select: none;
}
.task-card.completed .task-header,
.task-card.snoozed .task-header { cursor: pointer; }
.task-title {
  font-family: inherit; font-size: 1.02rem;
  font-weight: 600; color: var(--text);
  margin: 0 0 2px; line-height: 1.3;
  letter-spacing: -0.01em;
}
.task-plant {
  font-size: 0.82rem; color: var(--text-3);
  font-style: normal;
}
.task-due {
  display: inline-block; margin-top: 8px;
  font-size: 0.8rem; color: var(--text-3);
  font-weight: 500;
}
.task-due.overdue { color: var(--red); font-weight: 600; }
.task-snoozed-until {
  display: block; margin-top: 4px;
  font-size: 0.78rem; color: var(--text-3);
  font-style: normal;
}
.task-detail {
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transition: max-height 0.3s ease, opacity 0.25s ease;
  background: var(--bg-soft);
}
.task-card.expanded .task-detail {
  max-height: 1200px;
  opacity: 1;
}
.task-detail-section {
  padding: 14px 18px;
  border-bottom: 1px solid var(--border-soft);
}
.task-detail-section:last-child { border-bottom: none; }
.task-detail-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-3);
  font-weight: 600;
  margin-bottom: 4px;
}
.task-detail-text {
  font-size: 0.86rem;
  color: var(--text-2);
  line-height: 1.6;
}
.task-detail-text.task-howto {
  line-height: 1.7;
}
.task-detail-text.task-howto strong {
  color: var(--text);
  font-weight: 600;
  display: inline-block;
  margin-top: 2px;
}
.task-detail-text.task-howto br + strong {
  margin-top: 8px;
}
.task-actions {
  display: flex; gap: 6px;
  padding: 10px 12px 12px;
  border-top: 1px solid var(--border-soft);
  flex-wrap: wrap;
  justify-content: flex-end;
}
.task-btn {
  flex: 1; min-width: 90px;
  padding: 8px 12px;
  font-size: 0.83rem; font-weight: 500;
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  cursor: pointer; transition: all var(--t);
  display: inline-flex; align-items: center;
  justify-content: center; gap: 6px;
  background: var(--bg-card); color: var(--text-2);
}
.task-btn:hover { background: var(--bg-soft); border-color: var(--border-strong); }
.task-btn-done {
  background: var(--text); color: white; border-color: var(--text);
  font-size: 0.83rem;
  padding: 7px 14px;
  flex: 0 0 auto;
  min-width: 0;
  max-width: 30%;
  align-self: flex-end;
}
.task-btn-done:hover {
  background: #18181b; border-color: #18181b; color: white;
}

/* MODALS */
.modal {
  display: none; position: fixed; inset: 0;
  background: rgba(9, 9, 11, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 2000; align-items: center;
  justify-content: center; padding: 20px;
}
.modal.active { display: flex; animation: fadeIn 0.18s ease; }
.modal-content {
  background: var(--bg-card);
  border-radius: var(--r-xl);
  padding: 28px;
  max-width: 460px; width: 100%;
  max-height: 90vh; overflow-y: auto;
  box-shadow: var(--shadow-lg);
  position: relative;
  border: 1px solid var(--border);
}
.modal-content.modal-wide { max-width: 600px; }
.modal-close {
  position: absolute; top: 14px; right: 14px;
  background: transparent;
  border: 1px solid var(--border);
  width: 32px; height: 32px;
  border-radius: var(--r-md);
  cursor: pointer; font-size: 0.9rem;
  color: var(--text-3);
  transition: all var(--t);
  display: inline-flex; align-items: center; justify-content: center;
}
.modal-close:hover {
  background: var(--text); color: white; border-color: var(--text);
}
.modal h3 {
  font-family: inherit; margin: 0 0 14px;
  color: var(--text); font-size: 1.2rem;
  font-weight: 700; letter-spacing: -0.02em;
}
.snooze-task-name, .whatsapp-task-name {
  background: var(--bg-soft);
  border: 1px solid var(--border-soft);
  padding: 10px 14px; border-radius: var(--r-md);
  font-size: 0.85rem; color: var(--text-2);
  margin-bottom: 18px; font-style: normal; font-weight: 500;
}
.snooze-options {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 8px; margin-bottom: 18px;
}
.snooze-opt {
  padding: 11px 12px; font-size: 0.88rem;
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--bg-card);
  border-radius: var(--r-md);
  transition: all var(--t);
  color: var(--text-2); font-weight: 500;
  text-align: center;
}
.snooze-opt:hover {
  background: var(--bg-soft); border-color: var(--text); color: var(--text);
}
.snooze-custom {
  border-top: 1px solid var(--border-soft);
  padding-top: 16px;
  display: flex; flex-direction: column; gap: 8px;
}
.snooze-custom label {
  font-size: 0.78rem; color: var(--text-3);
  font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.05em;
}
.snooze-custom input[type="date"] {
  padding: 10px 14px; font-size: 0.9rem;
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  background: var(--bg-card); color: var(--text);
  transition: border-color var(--t);
}
.snooze-custom input[type="date"]:focus {
  outline: none; border-color: var(--text);
}
.btn-primary {
  background: var(--text); color: white;
  border: 1px solid var(--text);
  padding: 10px 16px;
  font-size: 0.88rem; font-weight: 600;
  border-radius: var(--r-md);
  cursor: pointer; transition: all var(--t);
}
.btn-primary:hover { background: #18181b; border-color: #18181b; }
.btn-primary:disabled {
  opacity: 0.4; cursor: not-allowed;
  background: var(--text-muted); border-color: var(--text-muted);
}
.btn-primary.btn-wa { background: var(--whatsapp); border-color: var(--whatsapp); }
.btn-primary.btn-wa:hover { background: var(--whatsapp-hover); border-color: var(--whatsapp-hover); }
.btn-secondary {
  background: var(--bg-card); color: var(--text-2);
  border: 1px solid var(--border);
  padding: 10px 16px;
  font-size: 0.88rem; font-weight: 500;
  border-radius: var(--r-md);
  cursor: pointer; transition: all var(--t);
}
.btn-secondary:hover { background: var(--bg-soft); border-color: var(--border-strong); }
.whatsapp-section { margin-bottom: 18px; }
.whatsapp-label {
  display: block; font-size: 0.78rem;
  color: var(--text-3); font-weight: 600;
  margin-bottom: 8px;
  text-transform: uppercase; letter-spacing: 0.05em;
}
.whatsapp-contacts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 8px;
}
.wa-contact-btn {
  padding: 12px 8px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  cursor: pointer; transition: all var(--t);
  font-size: 0.82rem; color: var(--text-2);
  text-align: center;
}
.wa-contact-btn:hover { background: var(--bg-soft); border-color: var(--border-strong); }
.wa-contact-btn.active {
  background: var(--whatsapp); color: white;
  border-color: var(--whatsapp);
}
.wa-contact-icon { font-size: 1.3rem; display: block; margin-bottom: 4px; }
.wa-contact-name { font-size: 0.76rem; line-height: 1.3; font-weight: 500; }
.wa-contact-noPhone {
  color: var(--red); font-size: 0.66rem;
  display: block; margin-top: 2px; font-weight: 500;
}
.whatsapp-message {
  width: 100%; padding: 12px 14px;
  font-size: 0.9rem;
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  resize: vertical; line-height: 1.5;
  background: var(--bg-card); color: var(--text);
  transition: border-color var(--t);
  font-family: inherit;
}
.whatsapp-message:focus { outline: none; border-color: var(--text); }
.whatsapp-actions { display: flex; justify-content: flex-end; }
.contacts-intro {
  font-size: 0.85rem; color: var(--text-3);
  margin-bottom: 16px; line-height: 1.55;
}
.contact-row {
  background: var(--bg-soft);
  border: 1px solid var(--border-soft);
  border-radius: var(--r-md);
  padding: 14px; margin-bottom: 10px;
}
.contact-row-header {
  display: flex; align-items: center;
  gap: 8px; margin-bottom: 10px;
}
.contact-row-icon { font-size: 1.3rem; }
.contact-row-name {
  font-weight: 600; color: var(--text);
  flex: 1; font-size: 0.95rem;
}
.contact-input {
  width: 100%; padding: 8px 12px;
  font-size: 0.86rem;
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  background: var(--bg-card);
  margin-bottom: 6px; color: var(--text);
  transition: border-color var(--t);
  font-family: inherit;
}
.contact-input:focus { outline: none; border-color: var(--text); }
.contact-input-label {
  font-size: 0.72rem; color: var(--text-3);
  font-weight: 600; margin-top: 6px; display: block;
  text-transform: uppercase; letter-spacing: 0.04em;
}
.contact-input.template { resize: vertical; min-height: 60px; line-height: 1.5; }
.contacts-footer {
  display: flex; justify-content: space-between;
  gap: 12px; margin-top: 18px;
  padding-top: 18px; border-top: 1px solid var(--border-soft);
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .container { padding: 20px 16px 60px; }
  .container-zones { padding-top: 20px; }
  h1.brand { font-size: 2.5rem; }
  .tab-btn { padding: 11px 6px; font-size: 0.82rem; gap: 4px; }
  .tab-emoji { font-size: 0.95rem; }
  .subtab-btn { padding: 7px 10px; font-size: 0.78rem; }
  .care-grid { grid-template-columns: 1fr; }
  .hbar { grid-template-columns: 80px 1fr; }
  .filter-bar { flex-direction: column; align-items: stretch; }
  .timeline-controls { flex-direction: column; align-items: stretch; }
  .task-photo, .task-photo-placeholder { width: 56px; height: 56px; }
  .task-btn { min-width: 0; }
  .task-btn-done { max-width: 45%; font-size: 0.8rem; padding: 6px 12px; }
  .task-side-hint { padding: 0 9px; gap: 4px; }
  .task-side-hint .hint-arrow { font-size: 1.2rem; }
  .task-side-hint .hint-icon { font-size: 0.95rem; }
  .task-header { padding: 14px 12px; }
  .task-detail-section { padding: 12px 14px; }
  .modal-content { padding: 20px; border-radius: var(--r-lg); }
  .snooze-options { grid-template-columns: 1fr 1fr; }
  .timeline-summary { gap: 20px; padding: 14px 18px; }
  .timeline-summary .stat-num { font-size: 1.4rem; }
  .mini-stats { gap: 16px; }
}
@media (max-width: 480px) {
  h1.brand { font-size: 2rem; }
  .cards-grid { gap: 12px; }
  .card-photo-wrap { height: 180px; }
  .tab-emoji { font-size: 1.05rem; }
  .tab-label { font-size: 0.82rem; }
  .tab-btn { padding: 10px 8px; gap: 5px; }
}
"""
