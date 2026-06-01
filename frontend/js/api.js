const API_BASE = '';

async function api(path, options = {}) {
  const token = localStorage.getItem('scs_token');
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem('scs_token');
    localStorage.removeItem('scs_user');
    window.location.href = '/index.html';
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Error ${res.status}`);
  }

  return res.json();
}

async function apiForm(path, formData) {
  const token = localStorage.getItem('scs_token');
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { method: 'POST', headers, body: formData });
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}
