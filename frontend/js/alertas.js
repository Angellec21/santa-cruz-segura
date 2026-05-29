requireAuth();

const user = getUser();
const puedeCrear = user?.id_rol === 2 || user?.id_rol === 4;

if (user?.id_rol === 4) document.getElementById('link-admin')?.classList.remove('d-none');
if (puedeCrear) document.getElementById('btn-nueva-alerta')?.classList.remove('d-none');

const TIPO_CONFIG = {
  preventiva:  { cls: 'tipo-preventiva', iconCls: 'icon-preventiva', icon: 'bi-shield-check', badgeCls: 'badge-tipo-preventiva' },
  reactiva:    { cls: 'tipo-reactiva',   iconCls: 'icon-reactiva',   icon: 'bi-exclamation-triangle-fill', badgeCls: 'badge-tipo-reactiva' },
  informativa: { cls: 'tipo-informativa',iconCls: 'icon-informativa', icon: 'bi-info-circle-fill', badgeCls: 'badge-tipo-informativa' },
};

async function cargarAlertas() {
  const lista = document.getElementById('alertas-list');
  try {
    const alertas = await api('/alertas');
    if (!alertas.length) {
      lista.innerHTML = `
        <div class="col-12 empty-state">
          <i class="bi bi-bell-slash"></i>
          <p class="fw-semibold mb-1" style="color:#f1f5f9">Sin alertas activas</p>
          <p style="font-size:.83rem;color:#64748b">No hay alertas activas en este momento.</p>
        </div>`;
      return;
    }
    lista.innerHTML = alertas.map(a => {
      const cfg = TIPO_CONFIG[a.tipo] || TIPO_CONFIG.informativa;
      const fecha = new Date(a.fecha_inicio).toLocaleDateString('es-BO', { day:'2-digit', month:'short', year:'numeric' });
      return `
      <div class="col-md-6 col-xl-4">
        <div class="alerta-card ${cfg.cls}">
          <div class="d-flex align-items-start gap-3">
            <div class="alerta-tipo-icon ${cfg.iconCls}">
              <i class="bi ${cfg.icon}"></i>
            </div>
            <div class="flex-grow-1 min-w-0">
              <div class="d-flex align-items-center gap-2 mb-2 flex-wrap">
                <span class="${cfg.badgeCls}">${a.tipo}</span>
                <span style="font-size:.72rem;color:#94a3b8;margin-left:auto">${fecha}</span>
              </div>
              <div style="font-weight:700;font-size:.9rem;color:#f1f5f9;margin-bottom:.3rem">${a.titulo || 'Sin título'}</div>
              <p style="font-size:.8rem;color:#94a3b8;margin:0 0 .65rem;line-height:1.5">${a.descripcion || 'Sin descripción adicional.'}</p>
              ${puedeCrear ? `
                <button onclick="cerrarAlerta(${a.id_alerta}, this)" class="btn-cerrar-alerta">
                  <i class="bi bi-check2-circle me-1"></i>Marcar resuelta
                </button>` : ''}
            </div>
          </div>
        </div>
      </div>`;
    }).join('');
  } catch {
    lista.innerHTML = '<div class="col-12"><div class="alert alert-danger">Error al cargar alertas.</div></div>';
  }
}

async function cerrarAlerta(id, btn) {
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
  await api(`/alertas/${id}/cerrar`, { method: 'PUT' });
  cargarAlertas();
}

async function cargarSelectsAlerta() {
  try {
    const [zonas, juntas] = await Promise.all([api('/zonas'), fetch('http://localhost:8000/auth/juntas').then(r => r.json())]);
    const selZona = document.getElementById('alerta-zona');
    zonas.forEach(z => { const o = document.createElement('option'); o.value = z.id_zona; o.textContent = z.nombre; selZona.appendChild(o); });
    const selJunta = document.getElementById('alerta-junta');
    juntas.forEach(j => { const o = document.createElement('option'); o.value = j.id_junta; o.textContent = j.nombre; selJunta.appendChild(o); });
  } catch {}
}

document.getElementById('btn-crear-alerta')?.addEventListener('click', async () => {
  const errEl = document.getElementById('alerta-error');
  errEl.classList.add('d-none');
  const btn = document.getElementById('btn-crear-alerta');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Publicando…';
  try {
    await api('/alertas', {
      method: 'POST',
      body: JSON.stringify({
        titulo: document.getElementById('alerta-titulo').value,
        tipo: document.getElementById('alerta-tipo').value,
        id_zona: parseInt(document.getElementById('alerta-zona').value),
        id_junta: parseInt(document.getElementById('alerta-junta').value),
        descripcion: document.getElementById('alerta-desc').value || null,
        fecha_fin: document.getElementById('alerta-fin').value || null,
      }),
    });
    bootstrap.Modal.getInstance(document.getElementById('modalAlerta')).hide();
    document.getElementById('alerta-form').reset();
    cargarAlertas();
  } catch (ex) {
    errEl.textContent = ex.message;
    errEl.classList.remove('d-none');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-bell me-2"></i>Publicar alerta';
  }
});

cargarAlertas();
if (puedeCrear) cargarSelectsAlerta();
