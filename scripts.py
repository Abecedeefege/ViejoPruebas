"""
JavaScript del documento.
Incluye:
- Tabs y subtabs
- Lightbox
- Búsqueda y filtros
- Timeline (newsfeed estilo Tinder)
- Modal de snooze
- Modal de WhatsApp con contactos por perfil
- Modal de edición de contactos
- localStorage para estado de tareas y contactos
"""

JS = r"""
// ============================================================
// CONSTANTES
// ============================================================
// Logo oficial de WhatsApp (path SVG monocromo, hereda color via currentColor)
const WHATSAPP_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.247-.694.247-1.289.173-1.413z"/></svg>';

// ============================================================
// TAB SWITCHING (top-level: Todo / Frente / Fondo / Timeline)
// ============================================================
function setBodyZone(zone) {
  document.body.classList.remove('zone-todo', 'zone-frente', 'zone-fondo', 'zone-timeline');
  document.body.classList.add(`zone-${zone}`);
}

document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.zone-content').forEach(z => z.classList.remove('active'));
    btn.classList.add('active');
    const zone = btn.dataset.zone;
    document.querySelector(`.zone-content[data-zone="${zone}"]`).classList.add('active');
    setBodyZone(zone);
    window.scrollTo({top: 0, behavior: 'smooth'});
    if (zone === 'timeline') renderTimeline();
  });
});

// ============================================================
// SUBTAB SWITCHING (within zone)
// ============================================================
document.querySelectorAll('.zone-content').forEach(zoneEl => {
  zoneEl.querySelectorAll('.subtab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      zoneEl.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
      zoneEl.querySelectorAll('.subtab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const sub = btn.dataset.sub;
      zoneEl.querySelector(`.subtab-pane[data-sub="${sub}"]`).classList.add('active');
    });
  });
});

// ============================================================
// IMAGE LAZY LOADING (data-img)
// ============================================================
function loadImg(img) {
  const k = img.getAttribute('data-img');
  if (k && IMG[k] && !img.src) img.src = IMG[k];
}
document.querySelectorAll('img[data-img]').forEach(loadImg);

// ============================================================
// LIGHTBOX
// ============================================================
function setupLightbox(scope) {
  scope.querySelectorAll('img[data-action="lightbox"]').forEach(img => {
    if (img.dataset.lightboxBound) return;
    img.dataset.lightboxBound = '1';
    img.addEventListener('click', (e) => {
      e.stopPropagation();
      const k = img.getAttribute('data-img');
      if (k && IMG[k]) {
        document.getElementById('lightbox-img').src = IMG[k];
        document.getElementById('lightbox').classList.add('active');
      }
    });
  });
}
setupLightbox(document);
document.getElementById('lightbox').addEventListener('click', function() {
  this.classList.remove('active');
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.getElementById('lightbox').classList.remove('active');
    document.querySelectorAll('.modal.active').forEach(m => m.classList.remove('active'));
  }
});

// ============================================================
// SEARCH + TAG FILTERS (zone view)
// ============================================================
document.querySelectorAll('.search').forEach(input => {
  input.addEventListener('input', () => {
    const pane = input.closest('.subtab-pane');
    if (!pane) return;
    const q = input.value.toLowerCase().trim();
    pane.querySelectorAll('.plant-card, .care-card, .idea-card, .huerta-card').forEach(card => {
      const name = card.dataset.name || '';
      const tags = card.dataset.tags || '';
      const visible = !q || name.includes(q) || tags.includes(q);
      card.style.display = visible ? '' : 'none';
    });
  });
});

document.querySelectorAll('.filter-tags').forEach(filterBar => {
  // Skip timeline filter — handled separately
  if (filterBar.classList.contains('timeline-filters')) return;
  filterBar.querySelectorAll('.ftag').forEach(btn => {
    btn.addEventListener('click', () => {
      filterBar.querySelectorAll('.ftag').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      const pane = filterBar.closest('.subtab-pane');
      if (!pane) return;
      pane.querySelectorAll('.plant-card').forEach(card => {
        const tags = card.dataset.tags || '';
        const visible = filter === 'all' || tags.includes(filter);
        card.style.display = visible ? '' : 'none';
      });
    });
  });
});

// ============================================================
// TIMELINE — STATE MANAGEMENT (localStorage)
// ============================================================
const STATE_KEY = 'jardineando_task_states_v1';
const CONTACTS_KEY = 'jardineando_contacts_v1';

function loadStates() {
  try { return JSON.parse(localStorage.getItem(STATE_KEY) || '{}'); }
  catch { return {}; }
}
function saveStates(states) {
  localStorage.setItem(STATE_KEY, JSON.stringify(states));
}
function getTaskState(taskId) {
  const states = loadStates();
  return states[taskId] || { status: 'active', snoozed_until: null, completed_at: null };
}
function setTaskState(taskId, state) {
  const states = loadStates();
  states[taskId] = state;
  saveStates(states);
}

function loadContacts() {
  try {
    const stored = localStorage.getItem(CONTACTS_KEY);
    if (stored) return JSON.parse(stored);
  } catch {}
  return JSON.parse(JSON.stringify(DEFAULT_CONTACTS));  // copia profunda
}
function saveContacts(contacts) {
  localStorage.setItem(CONTACTS_KEY, JSON.stringify(contacts));
}

// ============================================================
// TIMELINE — RENDERING
// ============================================================
let currentFilter = 'active';

function classifyTask(task) {
  const st = getTaskState(task.id);
  if (st.status === 'done') return 'done';
  if (st.status === 'snoozed') {
    const until = new Date(st.snoozed_until);
    if (!isNaN(until) && until > new Date()) return 'snoozed';
    // snooze expirado → vuelve a activa
    return 'active';
  }
  return 'active';
}

function dueLabel(task) {
  if (!task.due_month || !task.due_year) return task.due_label || '';
  const monthNames = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
  return `${monthNames[task.due_month - 1]} ${task.due_year}`;
}

function isOverdue(task) {
  if (!task.due_month || !task.due_year) return false;
  const due = new Date(task.due_year, task.due_month - 1, 28); // último día del mes objetivo
  return due < new Date();
}

function priorityInfo(p) {
  return ({
    'alta':  { emo: '🔴', color: '#dc2626', label: 'Alta' },
    'media': { emo: '🟡', color: '#ca8a04', label: 'Media' },
    'baja':  { emo: '🟢', color: '#16a34a', label: 'Baja' },
  })[p] || { emo: '⚪', color: '#6b6457', label: p };
}

function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('es-UY', { day: 'numeric', month: 'short', year: 'numeric' });
}

function renderTaskCard(task) {
  const st = getTaskState(task.id);
  const cls = classifyTask(task);
  const prio = priorityInfo(task.priority);
  const overdue = isOverdue(task);

  const photoHtml = task.plant_photo && IMG[task.plant_photo]
    ? `<img class="task-photo" data-img="${task.plant_photo}" data-action="lightbox" alt="">`
    : `<div class="task-photo-placeholder">🌱</div>`;

  let statusPill = '';
  if (cls === 'done') {
    statusPill = `<span class="task-status-pill done">✅ Hecha · ${fmtDate(st.completed_at)}</span>`;
  } else if (cls === 'snoozed') {
    statusPill = `<span class="task-status-pill snoozed">😴 Pospuesta hasta ${fmtDate(st.snoozed_until)}</span>`;
  }

  // Solo "Hecho" / "Reactivar" como botones — snooze y whatsapp se hacen por swipe
  let actions = '';
  if (cls === 'active') {
    actions = `
      <div class="task-actions">
        <button class="task-btn task-btn-done" data-action="done" data-task-id="${task.id}">✅ Marcar como hecho</button>
      </div>`;
  } else {
    actions = `
      <div class="task-actions">
        <button class="task-btn task-btn-undo" data-action="reactivate" data-task-id="${task.id}">↺ Reactivar</button>
      </div>`;
  }

  const dueClass = overdue && cls === 'active' ? 'overdue' : '';
  const dueText = task.due_label || dueLabel(task);

  // Sección expandible con detalle + por qué + cómo
  const fmtMd = (s) => (s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');

  const howToHtml = task.how_to
    ? `<div class="task-detail-section">
        <div class="task-detail-label">🛠️ Cómo hacerlo bien</div>
        <div class="task-detail-text task-howto">${fmtMd(task.how_to)}</div>
      </div>`
    : '';

  const detailHtml = `
    <div class="task-detail">
      <div class="task-detail-section">
        <div class="task-detail-label">💡 Por qué hacerlo</div>
        <div class="task-detail-text">${task.why || 'Sin justificación adicional.'}</div>
      </div>
      ${howToHtml}
    </div>`;

  // Side hints — solo para tareas activas (no se pueden swipear las done/snoozed)
  const sideHintLeft = (cls === 'active') ? `
    <div class="task-side-hint left" aria-label="Deslizar a la izquierda para posponer">
      <span class="hint-arrow">‹</span>
      <span class="hint-icon">😴</span>
    </div>` : '';
  const sideHintRight = (cls === 'active') ? `
    <div class="task-side-hint right" aria-label="Deslizar a la derecha para WhatsApp">
      <span class="hint-icon">${WHATSAPP_SVG}</span>
      <span class="hint-arrow">›</span>
    </div>` : '';

  return `
    <article class="task-card priority-${task.priority} ${cls === 'done' ? 'completed' : ''} ${cls === 'snoozed' ? 'snoozed' : ''}"
             data-task-id="${task.id}" style="--swipe-strength: 0">
      ${sideHintLeft}
      <div class="task-content-wrap">
        <div class="task-header">
          ${photoHtml}
          <div class="task-meta">
            <div class="task-meta-top">
              <span class="task-priority-pill" style="background: ${prio.color}">${prio.emo} ${prio.label}</span>
              <span class="task-zone-pill">${task.plant_codes.join(', ')}</span>
              ${statusPill}
              <span class="task-expand-chevron" aria-hidden="true">▾</span>
            </div>
            <h3 class="task-title">${task.title}</h3>
            <div class="task-plant">${task.plant_common}</div>
            ${dueText ? `<div class="task-due ${dueClass}">📅 ${overdue && cls === 'active' ? 'Vencida — ' : ''}${dueText}</div>` : ''}
          </div>
        </div>
        ${detailHtml}
        ${actions}
      </div>
      ${sideHintRight}
    </article>`;
}

function renderTimeline() {
  const feed = document.getElementById('timeline-feed');
  const empty = document.getElementById('timeline-empty');
  const summary = document.getElementById('timeline-summary');

  // Clasificar todas las tareas
  const buckets = { active: [], snoozed: [], done: [], all: [] };
  TASKS.forEach(task => {
    const cls = classifyTask(task);
    buckets[cls].push(task);
    buckets.all.push(task);
  });

  // Resumen
  summary.innerHTML = `
    <div class="stat-block"><div class="stat-num">${buckets.active.length}</div><div class="stat-label">📌 Activas</div></div>
    <div class="stat-block"><div class="stat-num">${buckets.done.length}</div><div class="stat-label">✅ Hechas</div></div>
    <div class="stat-block"><div class="stat-num">${buckets.snoozed.length}</div><div class="stat-label">😴 Pospuestas</div></div>
  `;

  // Render filtered feed
  const tasks = buckets[currentFilter] || [];

  if (tasks.length === 0) {
    feed.innerHTML = '';
    empty.style.display = 'block';
  } else {
    empty.style.display = 'none';
    feed.innerHTML = tasks.map(renderTaskCard).join('');
    // hidratar imágenes y bind swipe + lightbox
    feed.querySelectorAll('img[data-img]').forEach(loadImg);
    setupLightbox(feed);
    setupTaskInteractions(feed);
  }
}

// ============================================================
// TIMELINE — TASK INTERACTIONS (clicks + swipe)
// ============================================================
function setupTaskInteractions(scope) {
  // Click handlers para botones de acción
  scope.querySelectorAll('button[data-action]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const action = btn.dataset.action;
      const taskId = btn.dataset.taskId;
      const task = TASKS.find(t => t.id === taskId);
      if (!task) return;
      if (action === 'done') markDone(task);
      else if (action === 'snooze') openSnoozeModal(task);
      else if (action === 'whatsapp') openWhatsAppModal(task);
      else if (action === 'reactivate') reactivateTask(task);
    });
  });

  // Click en task-header para expandir/colapsar.
  // Se ignora si:
  //   - el target es un botón (los maneja el handler de arriba)
  //   - el target es la foto (se abre lightbox)
  //   - hubo swipe reciente (flag justSwiped seteada por setupSwipe)
  scope.querySelectorAll('.task-card').forEach(card => {
    const header = card.querySelector('.task-header');
    if (!header) return;
    header.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      if (e.target.closest('img')) return;
      if (card.dataset.justSwiped === '1') return;
      card.classList.toggle('expanded');
    });
  });

  // Swipe en cada card
  scope.querySelectorAll('.task-card').forEach(card => {
    setupSwipe(card);
  });
}

function setupSwipe(card) {
  // Solo tareas activas se pueden swipear
  if (card.classList.contains('completed') || card.classList.contains('snoozed')) return;

  let startX = 0, startY = 0, currentX = 0;
  let isDragging = false;
  let pointerDown = false;

  function onStart(x, y) {
    pointerDown = true;
    startX = x;
    startY = y;
    currentX = x;
    isDragging = false;
  }

  function onMove(x, y) {
    if (!pointerDown) return;
    const dx = x - startX;
    const dy = y - startY;
    if (!isDragging) {
      // determinar si es swipe horizontal vs scroll vertical
      if (Math.abs(dx) > 12 && Math.abs(dx) > Math.abs(dy)) {
        isDragging = true;
        card.classList.add('swiping');
      } else if (Math.abs(dy) > 12) {
        // scroll vertical, abandonar
        pointerDown = false;
        return;
      } else {
        return;
      }
    }
    currentX = x;
    const strength = Math.min(Math.abs(dx) / 120, 1);
    card.style.transform = `translateX(${dx}px) rotate(${dx * 0.05}deg)`;
    card.style.setProperty('--swipe-strength', strength);
    card.dataset.dxPositive = dx > 0;
    card.dataset.dxNegative = dx < 0;
  }

  function onEnd() {
    if (!pointerDown) return;
    pointerDown = false;
    if (!isDragging) return;
    const dx = currentX - startX;
    card.classList.remove('swiping');

    // Marcar flag para que el click handler ignore este "click" residual
    card.dataset.justSwiped = '1';
    setTimeout(() => { delete card.dataset.justSwiped; }, 350);

    const taskId = card.dataset.taskId;
    const task = TASKS.find(t => t.id === taskId);

    if (Math.abs(dx) > 100 && task) {
      if (dx > 0) {
        // swipe derecha → abrir modal WhatsApp
        card.style.transform = '';
        card.style.setProperty('--swipe-strength', 0);
        openWhatsAppModal(task);
      } else {
        // swipe izquierda → modal snooze
        card.style.transform = '';
        card.style.setProperty('--swipe-strength', 0);
        openSnoozeModal(task);
      }
    } else {
      // volver a posición
      card.style.transform = '';
      card.style.setProperty('--swipe-strength', 0);
    }
    delete card.dataset.dxPositive;
    delete card.dataset.dxNegative;
  }

  // Touch
  card.addEventListener('touchstart', (e) => {
    if (e.target.closest('button')) return;
    onStart(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: true });
  card.addEventListener('touchmove', (e) => {
    onMove(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: true });
  card.addEventListener('touchend', onEnd);
  card.addEventListener('touchcancel', onEnd);

  // Mouse (para testing en desktop)
  card.addEventListener('mousedown', (e) => {
    if (e.target.closest('button')) return;
    onStart(e.clientX, e.clientY);
  });
  document.addEventListener('mousemove', (e) => {
    if (pointerDown) onMove(e.clientX, e.clientY);
  });
  document.addEventListener('mouseup', () => {
    if (pointerDown) onEnd();
  });
}

// ============================================================
// TIMELINE — TASK ACTIONS
// ============================================================
function markDone(task) {
  setTaskState(task.id, {
    status: 'done',
    snoozed_until: null,
    completed_at: new Date().toISOString(),
  });
  setTimeout(renderTimeline, 100);
}

function reactivateTask(task) {
  setTaskState(task.id, { status: 'active', snoozed_until: null, completed_at: null });
  renderTimeline();
}

function snoozeTask(task, untilDate) {
  setTaskState(task.id, {
    status: 'snoozed',
    snoozed_until: untilDate,
    completed_at: null,
  });
  renderTimeline();
}

// ============================================================
// SNOOZE MODAL
// ============================================================
let pendingSnoozeTask = null;

function openSnoozeModal(task) {
  pendingSnoozeTask = task;
  document.getElementById('snooze-task-name').textContent = `📌 ${task.title} (${task.plant_common})`;
  document.getElementById('snooze-modal').classList.add('active');
  // pre-llenar fecha custom con hoy + 7
  const d = new Date(); d.setDate(d.getDate() + 7);
  document.getElementById('snooze-custom-date').valueAsDate = d;
}

document.querySelectorAll('.snooze-opt').forEach(btn => {
  btn.addEventListener('click', () => {
    if (!pendingSnoozeTask) return;
    const days = parseInt(btn.dataset.days, 10);
    const until = new Date();
    until.setDate(until.getDate() + days);
    snoozeTask(pendingSnoozeTask, until.toISOString());
    closeModal('snooze');
  });
});

document.getElementById('btn-snooze-custom').addEventListener('click', () => {
  if (!pendingSnoozeTask) return;
  const dateStr = document.getElementById('snooze-custom-date').value;
  if (!dateStr) return;
  const d = new Date(dateStr);
  if (d <= new Date()) { alert('Elegí una fecha futura'); return; }
  snoozeTask(pendingSnoozeTask, d.toISOString());
  closeModal('snooze');
});

// ============================================================
// WHATSAPP MODAL
// ============================================================
let pendingWaTask = null;
let pendingWaContactId = null;

function openWhatsAppModal(task) {
  pendingWaTask = task;
  pendingWaContactId = task.suggested_contact || null;
  document.getElementById('whatsapp-task-name').textContent = `📌 ${task.title} (${task.plant_common})`;
  renderWhatsAppContacts();
  // pre-llenar mensaje si hay contacto sugerido
  if (pendingWaContactId) {
    fillWhatsAppMessage(pendingWaContactId, task);
  } else {
    document.getElementById('whatsapp-message').value = '';
    document.getElementById('btn-send-whatsapp').disabled = true;
  }
  document.getElementById('whatsapp-modal').classList.add('active');
}

function renderWhatsAppContacts() {
  const contacts = loadContacts();
  const container = document.getElementById('whatsapp-contacts');
  container.innerHTML = contacts.map(c => {
    const noPhone = !c.phone || c.phone.trim() === '';
    return `
      <button class="wa-contact-btn ${pendingWaContactId === c.id ? 'active' : ''}" data-cid="${c.id}">
        <span class="wa-contact-icon">${c.icon}</span>
        <span class="wa-contact-name">${c.name}</span>
        ${noPhone ? '<span class="wa-contact-noPhone">(sin teléfono)</span>' : ''}
      </button>
    `;
  }).join('');
  container.querySelectorAll('.wa-contact-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      pendingWaContactId = btn.dataset.cid;
      renderWhatsAppContacts();
      fillWhatsAppMessage(pendingWaContactId, pendingWaTask);
    });
  });
}

function fillWhatsAppMessage(contactId, task) {
  const contacts = loadContacts();
  const c = contacts.find(x => x.id === contactId);
  if (!c) return;
  const taskText = `${task.title} — ${task.plant_common} (${task.plant_codes.join(', ')})`;
  const taskLink = SITE_URL ? `${SITE_URL}/tasks/${task.id}.html` : '';

  let msg = (c.default_template || '').replace(/\{task\}/g, taskText);
  if (msg.includes('{link}')) {
    msg = msg.replace(/\{link\}/g, taskLink || '(link no disponible)');
  } else if (taskLink) {
    // Si la plantilla no incluye {link}, lo agregamos al final automáticamente.
    msg = msg + '\n\n📎 ' + taskLink;
  }

  document.getElementById('whatsapp-message').value = msg;
  document.getElementById('btn-send-whatsapp').disabled = !c.phone || c.phone.trim() === '';
}

document.getElementById('btn-send-whatsapp').addEventListener('click', () => {
  if (!pendingWaTask || !pendingWaContactId) return;
  const contacts = loadContacts();
  const c = contacts.find(x => x.id === pendingWaContactId);
  if (!c || !c.phone) {
    alert('Este contacto no tiene teléfono. Editalo desde "📞 Mis contactos".');
    return;
  }
  const phone = c.phone.replace(/[^0-9]/g, '');
  const msg = document.getElementById('whatsapp-message').value;
  const url = `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`;
  window.open(url, '_blank');
  closeModal('whatsapp');
});

// ============================================================
// CONTACTS MODAL
// ============================================================
function openContactsModal() {
  renderContactsForm();
  document.getElementById('contacts-modal').classList.add('active');
}

function renderContactsForm() {
  const contacts = loadContacts();
  const list = document.getElementById('contacts-list');
  list.innerHTML = contacts.map((c, idx) => `
    <div class="contact-row" data-cid="${c.id}">
      <div class="contact-row-header">
        <span class="contact-row-icon">${c.icon}</span>
        <span class="contact-row-name">${c.name}</span>
      </div>
      <label class="contact-input-label">Teléfono (incluí código país, ej. +598 99 123 456)</label>
      <input type="tel" class="contact-input" data-field="phone" value="${(c.phone || '').replace(/"/g, '&quot;')}" placeholder="+598 99 123 456">
      <label class="contact-input-label">Plantilla del mensaje (usá {task} para insertar la tarea)</label>
      <textarea class="contact-input template" data-field="default_template" rows="3">${(c.default_template || '').replace(/</g,'&lt;')}</textarea>
    </div>
  `).join('');
}

document.getElementById('btn-edit-contacts').addEventListener('click', openContactsModal);

document.getElementById('btn-save-contacts').addEventListener('click', () => {
  const contacts = loadContacts();
  document.querySelectorAll('#contacts-list .contact-row').forEach(row => {
    const cid = row.dataset.cid;
    const c = contacts.find(x => x.id === cid);
    if (!c) return;
    c.phone = row.querySelector('[data-field="phone"]').value.trim();
    c.default_template = row.querySelector('[data-field="default_template"]').value;
  });
  saveContacts(contacts);
  closeModal('contacts');
  // refrescar modal whatsapp si está abierto
  if (pendingWaTask) renderWhatsAppContacts();
});

document.getElementById('btn-reset-contacts').addEventListener('click', () => {
  if (!confirm('¿Restaurar los contactos por defecto? Perderás los teléfonos guardados.')) return;
  saveContacts(JSON.parse(JSON.stringify(DEFAULT_CONTACTS)));
  renderContactsForm();
});

// ============================================================
// MODAL CLOSE HANDLERS
// ============================================================
function closeModal(name) {
  document.getElementById(`${name}-modal`).classList.remove('active');
}
document.querySelectorAll('.modal-close').forEach(btn => {
  btn.addEventListener('click', () => closeModal(btn.dataset.close));
});
document.querySelectorAll('.modal').forEach(modal => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.remove('active');
  });
});

// ============================================================
// TIMELINE FILTERS
// ============================================================
document.querySelectorAll('.timeline-filters .ftag').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.timeline-filters .ftag').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderTimeline();
  });
});

// ============================================================
// INIT
// ============================================================
renderTimeline();

// Si la URL trae #task=ID (viene de un share), abrir Timeline + expandir + scroll
function openTaskFromHash() {
  const m = (window.location.hash || '').match(/^#task=(.+)$/);
  if (!m) return;
  const taskId = decodeURIComponent(m[1]);
  // Switch a Timeline tab
  const tlBtn = document.querySelector('.tab-btn[data-zone="timeline"]');
  if (tlBtn && !tlBtn.classList.contains('active')) tlBtn.click();
  // Buscar la tarea — puede estar en filter "active" o no, así que vamos a "all"
  const task = TASKS.find(t => t.id === taskId);
  if (!task) return;
  // Cambiar al filtro "all" para asegurar que la veamos sea cual sea su estado
  const allBtn = document.querySelector('.timeline-filters .ftag[data-filter="all"]');
  if (allBtn) {
    document.querySelectorAll('.timeline-filters .ftag').forEach(b => b.classList.remove('active'));
    allBtn.classList.add('active');
    currentFilter = 'all';
    renderTimeline();
  }
  // Expandir y scroll después del render
  setTimeout(() => {
    const card = document.querySelector(`.task-card[data-task-id="${taskId}"]`);
    if (card) {
      card.classList.add('expanded');
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Highlight visual breve
      card.style.transition = 'box-shadow 0.4s ease';
      card.style.boxShadow = '0 0 0 3px rgba(21, 128, 61, 0.4)';
      setTimeout(() => { card.style.boxShadow = ''; }, 2200);
    }
  }, 200);
}
openTaskFromHash();
window.addEventListener('hashchange', openTaskFromHash);

// ============================================================
// CLIMA EN MONTEVIDEO (Open-Meteo, sin API key)
// ============================================================
function weatherCondition(code) {
  // WMO weather codes → emoji + label
  if (code === 0) return { emoji: '☀️', label: 'despejado' };
  if (code <= 2) return { emoji: '🌤️', label: 'algo nublado' };
  if (code === 3) return { emoji: '☁️', label: 'nublado' };
  if (code <= 48) return { emoji: '🌫️', label: 'niebla' };
  if (code <= 57) return { emoji: '🌦️', label: 'llovizna' };
  if (code <= 67) return { emoji: '🌧️', label: 'lluvia' };
  if (code <= 77) return { emoji: '🌨️', label: 'nieve' };
  if (code <= 82) return { emoji: '🌧️', label: 'chubascos' };
  if (code >= 95) return { emoji: '⛈️', label: 'tormenta' };
  return { emoji: '🌤️', label: '' };
}

async function loadWeather() {
  const el = document.getElementById('weather-line');
  if (!el) return;
  try {
    // Montevideo, Uruguay — coords
    const url = 'https://api.open-meteo.com/v1/forecast?latitude=-34.9011&longitude=-56.1645&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m&timezone=America%2FMontevideo';
    const r = await fetch(url, { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const data = await r.json();
    const c = data.current;
    const w = weatherCondition(c.weather_code);
    const temp = Math.round(c.temperature_2m);
    const wind = Math.round(c.wind_speed_10m);
    const hum = Math.round(c.relative_humidity_2m);
    el.innerHTML = `<span class="weather-emoji">${w.emoji}</span><span class="weather-text"><strong>${temp}°</strong> ${w.label} <span class="weather-sep">·</span> 💨 ${wind} km/h <span class="weather-sep">·</span> 💧 ${hum}% <span class="weather-sep">·</span> Montevideo</span>`;
  } catch (err) {
    el.innerHTML = '<span class="weather-emoji">🌱</span><span class="weather-text">Montevideo, Uruguay</span>';
  }
}
loadWeather();
"""
