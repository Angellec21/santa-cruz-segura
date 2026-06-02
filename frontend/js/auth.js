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
  // Gestionar reportes: directivo (2), autoridad (3), admin (4)
  if (user.id_rol >= 2) {
    document.getElementById('link-gestionar')?.classList.remove('d-none');
  }
  // Usuarios (admin): solo admin (4)
  if (user.id_rol === 4) {
    document.getElementById('link-admin')?.classList.remove('d-none');
  }
}

// Scripts están al final del body → DOM ya existe, ejecutar directo
initSidebarLinks();

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
