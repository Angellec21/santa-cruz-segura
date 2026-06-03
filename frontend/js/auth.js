function getToken() { return localStorage.getItem('scs_token'); }
function saveToken(token) { localStorage.setItem('scs_token', token); }

function getUser() {
  try { return JSON.parse(localStorage.getItem('scs_user')); } catch { return null; }
}

function requireAuth(allowedRoles = null) {
  const token = localStorage.getItem('scs_token');
  if (!token) { window.location.href = '/index.html'; return; }
  if (allowedRoles) {
    const user = getUser();
    const roleMap = { vecino: 1, directivo: 2, autoridad: 3, admin: 4 };
    const ok = allowedRoles.some(r => roleMap[r] === user?.id_rol);
    if (!ok) window.location.href = '/dashboard.html';
  }
}

document.getElementById('btn-logout')?.addEventListener('click', () => {
  localStorage.removeItem('scs_token');
  localStorage.removeItem('scs_user');
  window.location.href = '/index.html';
});

// Muestra links del sidebar según el rol del usuario
function initSidebarLinks() {
  const user = getUser();
  if (!user) return;
  const rol = Number(user.id_rol);

  if (rol === 3) {
    // Autoridad (policía): ocultar reportar y mis reportes, mostrar incidentes y mis casos
    document.getElementById('link-reportar')?.classList.add('d-none');
    document.getElementById('link-mis-reportes')?.classList.add('d-none');
    document.getElementById('link-incidentes')?.classList.remove('d-none');
    document.getElementById('link-mis-casos')?.classList.remove('d-none');
  } else {
    // Directivo, admin: gestionar reportes
    if (rol >= 2) {
      document.getElementById('link-gestionar')?.classList.remove('d-none');
    }
  }

  if (rol === 4) {
    document.getElementById('link-admin')?.classList.remove('d-none');
  }
}

// Scripts están al final del body → DOM ya existe, ejecutar directo
initSidebarLinks();

// Inyecta botón "Cambiar contraseña" antes del btn-logout en cualquier página
(function injectPasswordButton() {
  const logoutBtn = document.getElementById('btn-logout');
  if (!logoutBtn) return;
  const btn = document.createElement('button');
  btn.onclick = abrirCambiarPassword;
  btn.style.cssText = 'background:none;border:1px solid rgba(255,255,255,.07);color:#64748b;border-radius:7px;padding:.28rem .55rem;font-size:.73rem;cursor:pointer;transition:all .2s;font-family:Inter,sans-serif;width:100%;display:flex;align-items:center;justify-content:center;gap:.3rem;margin-bottom:.35rem;';
  btn.innerHTML = '<i class="bi bi-key"></i> Cambiar contraseña';
  btn.onmouseover = () => { btn.style.borderColor='#00d47a'; btn.style.color='#00d47a'; };
  btn.onmouseout  = () => { btn.style.borderColor='rgba(255,255,255,.07)'; btn.style.color='#64748b'; };
  logoutBtn.parentNode.insertBefore(btn, logoutBtn);
})()

// ── Modal cambiar contraseña — sin dependencia de Bootstrap JS ──
function injectPasswordModal() {
  if (document.getElementById('modal-cambiar-pass')) return;
  const html = `
  <div id="modal-cambiar-pass" onclick="if(event.target===this)cerrarPassModal()" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:9999;align-items:center;justify-content:center;backdrop-filter:blur(4px)">
    <div style="background:#081510;border:1px solid rgba(255,255,255,.1);border-radius:16px;width:100%;max-width:380px;margin:1rem;box-shadow:0 0 60px rgba(0,0,0,.6)">
      <div style="background:rgba(0,212,122,.08);border-bottom:1px solid rgba(0,212,122,.2);padding:.85rem 1.2rem;border-radius:16px 16px 0 0;display:flex;align-items:center;justify-content:space-between">
        <span style="color:#00d47a;font-weight:700;font-size:.9rem"><i class="bi bi-key me-2"></i>Cambiar contraseña</span>
        <button onclick="cerrarPassModal()" style="background:none;border:none;color:#64748b;cursor:pointer;font-size:1.1rem;line-height:1">✕</button>
      </div>
      <div style="padding:1.2rem">
        <div id="pass-err" style="display:none;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.2);color:#fca5a5;border-radius:8px;padding:.5rem .75rem;font-size:.8rem;margin-bottom:.75rem"></div>
        <div id="pass-ok"  style="display:none;background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.2);color:#6ee7b7;border-radius:8px;padding:.5rem .75rem;font-size:.8rem;margin-bottom:.75rem"></div>
        <div style="margin-bottom:.7rem">
          <label style="font-size:.75rem;font-weight:600;color:#94a3b8;display:block;margin-bottom:.3rem">Contraseña actual</label>
          <input type="password" id="pass-actual" placeholder="Tu contraseña actual"
            style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:.55rem .8rem;font-size:.85rem;color:#f1f5f9;font-family:Inter,sans-serif;box-sizing:border-box"/>
        </div>
        <div style="margin-bottom:.7rem">
          <label style="font-size:.75rem;font-weight:600;color:#94a3b8;display:block;margin-bottom:.3rem">Nueva contraseña</label>
          <input type="password" id="pass-nueva" placeholder="Mínimo 6 caracteres"
            style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:.55rem .8rem;font-size:.85rem;color:#f1f5f9;font-family:Inter,sans-serif;box-sizing:border-box"/>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:#94a3b8;display:block;margin-bottom:.3rem">Confirmar nueva contraseña</label>
          <input type="password" id="pass-confirmar" placeholder="Repite la nueva contraseña"
            style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:.55rem .8rem;font-size:.85rem;color:#f1f5f9;font-family:Inter,sans-serif;box-sizing:border-box"/>
        </div>
      </div>
      <div style="padding:.85rem 1.2rem;border-top:1px solid rgba(255,255,255,.07);display:flex;justify-content:flex-end;gap:.6rem">
        <button onclick="cerrarPassModal()" style="background:none;border:1px solid rgba(255,255,255,.12);color:#94a3b8;border-radius:7px;padding:.35rem .9rem;font-size:.82rem;cursor:pointer;font-family:Inter,sans-serif">Cancelar</button>
        <button id="btn-guardar-pass" onclick="guardarPassword()"
          style="background:linear-gradient(135deg,rgba(0,212,122,.9),rgba(0,212,122,.7));border:none;color:#060e0a;font-weight:700;padding:.35rem 1.1rem;border-radius:7px;font-size:.82rem;cursor:pointer;font-family:Inter,sans-serif">
          Guardar
        </button>
      </div>
    </div>
  </div>`;
  document.body.insertAdjacentHTML('beforeend', html);
}

function abrirCambiarPassword() {
  injectPasswordModal();
  document.getElementById('pass-err').style.display = 'none';
  document.getElementById('pass-ok').style.display  = 'none';
  document.getElementById('pass-actual').value    = '';
  document.getElementById('pass-nueva').value     = '';
  document.getElementById('pass-confirmar').value = '';
  document.getElementById('modal-cambiar-pass').style.display = 'flex';
  setTimeout(() => document.getElementById('pass-actual').focus(), 50);
}

function cerrarPassModal() {
  const el = document.getElementById('modal-cambiar-pass');
  if (el) el.style.display = 'none';
}

async function guardarPassword() {
  const errEl = document.getElementById('pass-err');
  const okEl  = document.getElementById('pass-ok');
  const actual    = document.getElementById('pass-actual').value;
  const nueva     = document.getElementById('pass-nueva').value;
  const confirmar = document.getElementById('pass-confirmar').value;
  errEl.style.display = 'none'; okEl.style.display = 'none';
  if (nueva !== confirmar) { errEl.textContent = 'Las contraseñas nuevas no coinciden.'; errEl.style.display = 'block'; return; }
  if (nueva.length < 6)    { errEl.textContent = 'La nueva contraseña debe tener al menos 6 caracteres.'; errEl.style.display = 'block'; return; }
  const btn = document.getElementById('btn-guardar-pass');
  btn.disabled = true; btn.textContent = 'Guardando…';
  try {
    await api('/usuarios/me/password', { method: 'PUT', body: JSON.stringify({ password_actual: actual, password_nueva: nueva }) });
    okEl.textContent = '¡Contraseña cambiada! Vuelve a iniciar sesión.';
    okEl.style.display = 'block';
    setTimeout(() => { localStorage.removeItem('scs_token'); localStorage.removeItem('scs_user'); window.location.href = '/index.html'; }, 2000);
  } catch(e) {
    errEl.textContent = e.message || 'Error al cambiar la contraseña.';
    errEl.style.display = 'block';
  } finally {
    btn.disabled = false; btn.textContent = 'Guardar';
  }
}

// ---- Login / Register (solo index.html) ----
const loginForm = document.getElementById('login-form');
if (loginForm) {
  if (localStorage.getItem('scs_token')) window.location.href = '/dashboard.html';

  loginForm.addEventListener('submit', async e => {
    e.preventDefault();
    const errEl = document.getElementById('login-error');
    errEl.classList.add('d-none');
    const btn = loginForm.querySelector('button[type=submit]');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Ingresando…';
    try {
      const data = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          email: document.getElementById('email').value,
          password: document.getElementById('password').value,
        }),
      });
      localStorage.setItem('scs_token', data.access_token);
      const me = await api('/usuarios/me');
      localStorage.setItem('scs_user', JSON.stringify(me));
      window.location.href = '/dashboard.html';
    } catch (ex) {
      errEl.textContent = ex.message;
      errEl.classList.remove('d-none');
      btn.disabled = false; btn.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Ingresar';
    }
  });

  document.getElementById('register-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    const errEl = document.getElementById('register-error');
    errEl.classList.add('d-none');
    const btn = e.target.querySelector('button[type=submit]');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creando cuenta…';
    try {
      await api('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          nombre: document.getElementById('reg-nombre').value,
          apellido: document.getElementById('reg-apellido').value,
          email: document.getElementById('reg-email').value,
          telefono: document.getElementById('reg-telefono').value || null,
          password: document.getElementById('reg-password').value,
          id_junta: parseInt(document.getElementById('reg-junta').value),
        }),
      });
      // Volver al login con el email prefilled
      document.getElementById('email').value = document.getElementById('reg-email').value;
      showTab('login');
      const alert = document.createElement('div');
      alert.className = 'alert alert-success py-2 small mt-2';
      alert.innerHTML = '<i class="bi bi-check-circle me-1"></i>Cuenta creada. Ya puedes ingresar.';
      loginForm.prepend(alert);
    } catch (ex) {
      errEl.textContent = ex.message;
      errEl.classList.remove('d-none');
    } finally {
      btn.disabled = false; btn.innerHTML = '<i class="bi bi-person-check me-2"></i>Crear cuenta';
    }
  });
}

async function cargarJuntas() {
  const sel = document.getElementById('reg-junta');
  if (!sel || sel.options.length > 1) return;
  try {
    const juntas = await fetch('/auth/juntas').then(r => r.json());
    juntas.forEach(j => {
      const opt = document.createElement('option');
      opt.value = j.id_junta; opt.textContent = j.nombre;
      sel.appendChild(opt);
    });
  } catch {}
}
