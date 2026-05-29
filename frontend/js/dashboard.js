requireAuth();

const user = getUser();
if (user?.id_rol === 4) document.getElementById('link-admin')?.classList.remove('d-none');

// Sidebar user info
if (user) {
  const ini = (user.nombre || '?')[0].toUpperCase();
  const avEl = document.getElementById('user-avatar');
  if (avEl) avEl.textContent = ini;
  const nmEl = document.getElementById('user-name');
  if (nmEl) nmEl.textContent = `${user.nombre || ''} ${user.apellido || ''}`.trim() || user.email;
  const rlEl = document.getElementById('user-role');
  if (rlEl) rlEl.textContent = { 1:'Vecino', 2:'Directivo', 3:'Autoridad', 4:'Admin' }[user.id_rol] || 'Usuario';
}

const NIVEL_COLOR = { bajo:'#34d399', medio:'#fbbf24', alto:'#f87171', critico:'#a78bfa' };
const NIVEL_CLASS = { bajo:'pb-bajo', medio:'pb-medio', alto:'pb-alto', critico:'pb-critico' };
const NIVEL_RB    = { bajo:'rb-bajo', medio:'rb-medio', alto:'rb-alto', critico:'rb-critico' };

function nivelNum(n) { return { bajo:0, medio:1, alto:2, critico:3 }[n] ?? 0; }

// ── Alert banner ──────────────────────────────────────────────────────────────
async function cargarAlertaBanner() {
  try {
    const alertas = await api('/alertas');
    if (!alertas.length) return;
    const banner = document.getElementById('alert-banner');
    const a = alertas[0];
    const cfg = {
      preventiva: ['#fef3c7','#d97706','bi-shield-check'],
      reactiva:   ['#fee2e2','#dc2626','bi-exclamation-triangle-fill'],
      informativa:['#dbeafe','#1d4ed8','bi-info-circle-fill'],
    };
    const [bg, color, icon] = cfg[a.tipo] || cfg.informativa;
    banner.innerHTML = `
      <div style="background:${bg};border-radius:14px;padding:1rem 1.25rem;margin-bottom:1.1rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
        <i class="bi ${icon} fs-4" style="color:${color};flex-shrink:0"></i>
        <div style="flex:1;min-width:0">
          <div style="font-weight:700;font-size:.87rem;color:#0f172a">${a.titulo}</div>
          ${a.descripcion ? `<div style="font-size:.79rem;color:#64748b">${a.descripcion}</div>` : ''}
        </div>
        <a href="alertas.html" style="background:${color};color:#fff;border-radius:8px;padding:.32rem .8rem;font-size:.77rem;font-weight:600;text-decoration:none;white-space:nowrap">
          Ver todas (${alertas.length})
        </a>
      </div>`;
  } catch {}
}

// ── Dashboard resumen ─────────────────────────────────────────────────────────
async function cargarResumen() {
  try {
    const resumen = await api('/dashboard/resumen');
    if (!resumen.length) return;

    const totales = resumen.reduce((acc, r) => {
      acc.reportes += r.reportes_30d || 0;
      acc.alertas  += r.alertas_activas || 0;
      acc.zonas++;
      if (nivelNum(r.nivel_riesgo_max) > nivelNum(acc.riesgo_max)) acc.riesgo_max = r.nivel_riesgo_max;
      return acc;
    }, { reportes:0, alertas:0, zonas:0, riesgo_max:'bajo' });

    document.getElementById('val-reportes').textContent = totales.reportes;
    document.getElementById('val-alertas').textContent  = totales.alertas;
    document.getElementById('val-zonas').textContent    = totales.zonas;

    const rEl = document.getElementById('val-riesgo');
    rEl.textContent = totales.riesgo_max;
    rEl.style.color = NIVEL_COLOR[totales.riesgo_max] || '#64748b';

    renderTabla(resumen);
  } catch {}
}

function renderTabla(resumen) {
  const tbody = document.querySelector('#tabla-barrios tbody');
  if (!tbody) return;
  tbody.innerHTML = resumen.map(r => {
    const cls = NIVEL_RB[r.nivel_riesgo_max] || 'rb-bajo';
    return `<tr>
      <td style="font-weight:600">${r.junta}</td>
      <td class="d-none-sm"><span style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);color:#94a3b8;font-size:.7rem;padding:.15rem .5rem;border-radius:6px">${r.distrito}</span></td>
      <td style="color:#f1f5f9">${r.reportes_30d || 0}</td>
      <td class="d-none-md" style="color:#f1f5f9">${r.alertas_activas || 0}</td>
      <td><span class="rb ${cls}">${r.nivel_riesgo_max || 'bajo'}</span></td>
    </tr>`;
  }).join('');
}

// ── Tendencia (line chart) ────────────────────────────────────────────────────
async function cargarTendencia() {
  try {
    const data = await api('/dashboard/tendencia');
    const ctx = document.getElementById('chart-tendencia');
    if (!ctx) return;

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(d => {
          const f = new Date(d.fecha + 'T00:00:00');
          return f.toLocaleDateString('es-BO', { day:'2-digit', month:'short' });
        }),
        datasets: [{
          label: 'Reportes',
          data: data.map(d => d.total),
          borderColor: '#00d47a',
          backgroundColor: 'rgba(0,212,122,.06)',
          borderWidth: 2,
          pointRadius: 3.5,
          pointBackgroundColor: '#00d47a',
          pointBorderColor: '#070d18',
          pointBorderWidth: 1.5,
          tension: 0.4,
          fill: true,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid:{ display:false }, ticks:{ font:{ size:10 }, maxRotation:0, maxTicksLimit:8, color:'#475569' } },
          y: { grid:{ color:'rgba(255,255,255,.04)' }, ticks:{ font:{ size:10 }, stepSize:1, color:'#475569' }, beginAtZero:true },
        },
      },
    });
  } catch {}
}

// ── Tipos (donut chart) ───────────────────────────────────────────────────────
async function cargarTipos() {
  try {
    const data = await api('/dashboard/tipos');
    const ctx = document.getElementById('chart-tipos');
    if (!ctx) return;

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.map(d => d.nombre),
        datasets: [{
          data: data.map(d => d.total),
          backgroundColor: ['#00d47a','#a78bfa','#34d399','#f87171','#fbbf24','#60a5fa'],
          borderWidth: 2,
          borderColor: '#070d18',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        cutout: '68%',
        plugins: {
          legend: { position:'bottom', labels:{ boxWidth:10, font:{ size:11 }, padding:12, color:'#64748b' } },
        },
      },
    });
  } catch {}
}

// ── IA Predicciones panel ─────────────────────────────────────────────────────
async function cargarPredicciones() {
  const container = document.getElementById('ai-zonas-list');
  if (!container) return;
  try {
    const [zonas, preds] = await Promise.all([
      api('/zonas'),
      api('/ia/predicciones').catch(() => []),
    ]);

    const predMap = {};
    preds.forEach(p => { predMap[p.id_zona] = p; });

    const puedePredir = user && [2, 3, 4].includes(user.id_rol);

    container.innerHTML = zonas.map(z => {
      const pred = predMap[z.id_zona];
      const actual = z.nivel_riesgo || 'bajo';
      const nivelPred = pred?.nivel_predicho || null;
      const prob = pred ? Math.round((pred.probabilidad || 0) * 100) : null;
      const color = NIVEL_COLOR[actual];

      return `<div class="zona-row">
        <div class="nivel-dot" style="background:${color}"></div>
        <div style="flex:1;min-width:0">
          <div class="zona-name text-truncate">${z.nombre}</div>
          <div class="zona-actual">Actual: <b style="color:${color}">${actual}</b></div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          ${nivelPred
            ? `<div><span class="pred-badge ${NIVEL_CLASS[nivelPred]}">${nivelPred}</span></div>
               <div class="pred-prob">${prob}% confianza</div>`
            : `<div class="pred-prob" style="color:#cbd5e1">Sin predicción</div>`}
          ${puedePredir
            ? `<button class="btn-pred mt-1" onclick="predecirZona(${z.id_zona},this)"><i class="bi bi-cpu"></i> Predecir</button>`
            : ''}
        </div>
      </div>`;
    }).join('');
  } catch {
    container.innerHTML = '<div class="text-center text-muted py-4" style="font-size:.82rem">No disponible</div>';
  }
}

window.predecirZona = async function(id_zona, btn) {
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm" style="width:.65rem;height:.65rem"></span>';
  try {
    await api(`/ia/predecir/${id_zona}`, { method:'POST' });
    await cargarPredicciones();
  } catch {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-cpu"></i> Predecir';
  }
};

// ── Init ──────────────────────────────────────────────────────────────────────
cargarAlertaBanner();
cargarResumen();
cargarTendencia();
cargarTipos();
cargarPredicciones();
