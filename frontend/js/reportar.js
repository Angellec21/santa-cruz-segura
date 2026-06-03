requireAuth();

const TIPO_ICONOS = {
  'Robo a domicilio':   'bi-house-exclamation',
  'Robo a transeúnte':  'bi-person-exclamation',
  'Hurto':              'bi-bag-x',
  'Violencia':          'bi-exclamation-octagon',
  'Persona sospechosa': 'bi-eye',
  'Vandalismo':         'bi-hammer',
  'Otro':               'bi-question-circle',
};
const COLOR_RIESGO = { bajo: '#22c55e', medio: '#eab308', alto: '#ef4444', critico: '#b91c1c' };
const FILL_OP_R    = { bajo: 0.13,    medio: 0.22,    alto: 0.32,    critico: 0.42 };

let lat = null, lng = null;
let marcador = null;
let tipoSeleccionado = null;
let zonasData = [];
let heatLayer = null;

const mapa = L.map('mapa-reportar', { zoomControl: false }).setView([-17.7834, -63.1821], 13);
L.control.zoom({ position: 'bottomright' }).addTo(mapa);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { attribution:'© CARTO', maxZoom: 19 }).addTo(mapa);
heatLayer = L.heatLayer([], { radius: 35, blur: 25, maxZoom: 17, gradient:{ 0.3:'#7c3aed', 0.6:'#00d47a', 0.8:'#f59e0b', 1.0:'#ef4444' } }).addTo(mapa);

// ── Distancia entre dos puntos GPS en metros (Haversine) ──────────────────
function distanciaMetros(lat1, lng1, lat2, lng2) {
  const R  = 6371000;
  const φ1 = lat1 * Math.PI / 180;
  const φ2 = lat2 * Math.PI / 180;
  const Δφ = (lat2 - lat1) * Math.PI / 180;
  const Δλ = (lng2 - lng1) * Math.PI / 180;
  const a  = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// ── Detecta la zona más cercana al punto clicado ──────────────────────────
function detectarZona(lat, lng) {
  let mejor = null;
  let distMin = Infinity;
  for (const z of zonasData) {
    const dist = distanciaMetros(lat, lng, parseFloat(z.latitud_centro), parseFloat(z.longitud_centro));
    if (dist < distMin) { distMin = dist; mejor = { zona: z, dist: Math.round(dist) }; }
  }
  return mejor;
}

// ── Indicador visual de zona detectada ───────────────────────────────────
function mostrarIndicadorZona(resultado) {
  const el = document.getElementById('zona-detectada-info');
  if (!el || !resultado) return;
  const { zona, dist } = resultado;
  const dentroDeZona = dist <= zona.radio_metros;
  const color = COLOR_RIESGO[zona.nivel_riesgo] || '#6c757d';

  if (dentroDeZona) {
    el.innerHTML = `
      <i class="bi bi-geo-alt-fill me-1" style="color:${color}"></i>
      Zona detectada: <strong>${zona.nombre}</strong>
      <span class="badge ms-1" style="background:${color};font-size:.65rem">${zona.nivel_riesgo}</span>`;
    el.className = 'small mt-1 text-success';
  } else {
    el.innerHTML = `
      <i class="bi bi-geo-alt me-1 text-warning"></i>
      Zona más cercana: <strong>${zona.nombre}</strong>
      <span class="text-muted">(~${dist} m)</span>`;
    el.className = 'small mt-1 text-warning';
  }
}

// ── Click en el mapa ──────────────────────────────────────────────────────
mapa.on('click', e => {
  lat = e.latlng.lat;
  lng = e.latlng.lng;

  document.getElementById('latitud-display').value  = lat.toFixed(6);
  document.getElementById('longitud-display').value = lng.toFixed(6);

  if (marcador) mapa.removeLayer(marcador);
  marcador = L.marker([lat, lng])
    .addTo(mapa)
    .bindPopup('<b>Ubicación seleccionada</b><br><small>Completa el formulario</small>')
    .openPopup();

  // Auto-detectar zona más cercana
  const resultado = detectarZona(lat, lng);
  if (resultado) {
    document.getElementById('zona').value = resultado.zona.id_zona;
    mostrarIndicadorZona(resultado);
  }

  const btn = document.getElementById('btn-abrir-reporte');
  btn.disabled = false;
  btn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Reportar aquí';
  document.getElementById('pin-hint').style.display = 'none';

  new bootstrap.Modal(document.getElementById('modalReporte')).show();
});

// ── Carga de selects y dibujo de zonas en el mapa ────────────────────────
async function cargarSelects() {
  try {
    const [tipos, zonas] = await Promise.all([
      fetch('/auth/tipos').then(r => r.json()),
      api('/zonas'),
    ]);

    // Guardar zonas para la auto-detección
    zonasData = zonas;

    // Cargar heatmap con puntos de todos los reportes existentes
    const puntosCalor = [];
    for (const z of zonas) {
      const pts = await api(`/zonas/${z.id_zona}/heatmap`);
      pts.forEach(p => puntosCalor.push([p.lat, p.lng, p.intensity]));
    }
    if (puntosCalor.length) heatLayer.setLatLngs(puntosCalor);

    // Dibujar zonas en el mapa de reporte con efecto calor
    zonas.forEach(z => {
      const color = COLOR_RIESGO[z.nivel_riesgo] || '#22c55e';
      const fo    = FILL_OP_R[z.nivel_riesgo]    || 0.13;

      // Halo exterior
      L.circle([parseFloat(z.latitud_centro), parseFloat(z.longitud_centro)], {
        radius: z.radio_metros * 1.12,
        color: color, fillColor: color,
        fillOpacity: fo * 0.3, weight: 0, opacity: 0,
        interactive: false,
      }).addTo(mapa);

      // Círculo principal — no interactivo para que los clics pasen al mapa
      L.circle([parseFloat(z.latitud_centro), parseFloat(z.longitud_centro)], {
        radius: z.radio_metros,
        color: color, fillColor: color,
        fillOpacity: fo, weight: 1.8, opacity: 0.8,
        interactive: false,
      }).addTo(mapa);

      // Núcleo central
      L.circle([parseFloat(z.latitud_centro), parseFloat(z.longitud_centro)], {
        radius: z.radio_metros * 0.38,
        color: 'transparent', fillColor: color,
        fillOpacity: Math.min(fo * 2.8, 0.75), weight: 0,
        interactive: false,
      }).addTo(mapa);

      // Etiqueta
      L.marker([parseFloat(z.latitud_centro), parseFloat(z.longitud_centro)], {
        icon: L.divIcon({
          className: '',
          html: `<div style="
            background:rgba(6,14,10,.82);color:${color};
            font-size:.62rem;font-weight:700;
            padding:.18rem .48rem;border-radius:8px;
            white-space:nowrap;border:1px solid ${color}44;
            box-shadow:0 0 8px ${color}44;
          ">${z.nombre}</div>`,
          iconAnchor: [0, 0],
        }),
        interactive: false, keyboard: false,
      }).addTo(mapa);
    });

    // Tipos de incidente como botones visuales
    const grid = document.getElementById('tipos-grid');
    tipos.forEach(t => {
      const icono = TIPO_ICONOS[t.nombre] || 'bi-flag';
      const col = document.createElement('div');
      col.className = 'col-6 col-md-4';
      col.innerHTML = `
        <div class="tipo-btn border rounded-3 p-2 text-center" data-id="${t.id_tipo}">
          <i class="bi ${icono} fs-5 d-block mb-1 text-secondary"></i>
          <small class="fw-semibold" style="font-size:.75rem;">${t.nombre}</small>
        </div>`;
      col.querySelector('.tipo-btn').addEventListener('click', function () {
        document.querySelectorAll('.tipo-btn').forEach(b => b.classList.remove('selected'));
        this.classList.add('selected');
        tipoSeleccionado = parseInt(this.dataset.id);
        document.getElementById('tipo-incidente').value = tipoSeleccionado;
      });
      grid.appendChild(col);
    });

    // Dropdown de zonas agrupado por distrito
    const selZona = document.getElementById('zona');
    const grupos = {};
    zonas.forEach(z => {
      const dist = z.distrito || 'Otros';
      if (!grupos[dist]) grupos[dist] = [];
      grupos[dist].push(z);
    });
    Object.keys(grupos).sort().forEach(dist => {
      const grp = document.createElement('optgroup');
      grp.label = dist;
      grupos[dist].forEach(z => {
        const o = document.createElement('option');
        o.value = z.id_zona;
        o.textContent = z.nombre;
        grp.appendChild(o);
      });
      selZona.appendChild(grp);
    });

    // Fecha por defecto = ahora
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('fecha-incidente').value = now.toISOString().slice(0, 16);

  } catch (e) { console.error('Error cargando selects:', e); }
}

// ── Enviar reporte ────────────────────────────────────────────────────────
document.getElementById('btn-enviar-reporte').addEventListener('click', async () => {
  const errEl = document.getElementById('reporte-error');
  const msgEl = document.getElementById('reporte-msg');
  errEl.classList.add('d-none');
  msgEl.classList.add('d-none');

  if (!lat || !lng) {
    errEl.textContent = 'Selecciona la ubicación en el mapa primero.';
    errEl.classList.remove('d-none');
    return;
  }
  if (!tipoSeleccionado) {
    errEl.textContent = 'Selecciona el tipo de incidente.';
    errEl.classList.remove('d-none');
    return;
  }
  const idZona = parseInt(document.getElementById('zona').value);
  if (!idZona) {
    errEl.textContent = 'Selecciona o confirma la zona del incidente.';
    errEl.classList.remove('d-none');
    return;
  }

  const btn = document.getElementById('btn-enviar-reporte');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Enviando…';

  try {
    const reporte = await api('/reportes', {
      method: 'POST',
      body: JSON.stringify({
        id_zona: idZona,
        id_tipo: tipoSeleccionado,
        descripcion: document.getElementById('descripcion').value || null,
        latitud: lat,
        longitud: lng,
        anonimo: document.getElementById('anonimo').checked,
        fecha_incidente: document.getElementById('fecha-incidente').value,
      }),
    });

    // Agregar el nuevo reporte al heatmap inmediatamente
    heatLayer.addLatLng([lat, lng, 0.9]);

    // Mostrar éxito del reporte antes de intentar subir evidencia
    msgEl.innerHTML = '<i class="bi bi-check-circle me-1"></i>Reporte enviado. Gracias por colaborar con tu barrio.';
    msgEl.classList.remove('d-none');

    // Subir evidencia (opcional) — si falla, el reporte ya está guardado
    const archivo = document.getElementById('evidencia').files[0];
    if (archivo) {
      try {
        const form = new FormData();
        form.append('archivo', archivo);
        await apiForm(`/reportes/${reporte.id_reporte}/evidencia`, form);
        msgEl.innerHTML += ' <i class="bi bi-paperclip ms-1"></i>Evidencia adjuntada.';
      } catch (evErr) {
        msgEl.innerHTML += `<br><small class="text-warning"><i class="bi bi-exclamation-triangle me-1"></i>Evidencia no subida: ${evErr.message}</small>`;
      }
    }

    setTimeout(() => {
      bootstrap.Modal.getInstance(document.getElementById('modalReporte')).hide();
      document.getElementById('reporte-form').reset();
      document.querySelectorAll('.tipo-btn').forEach(b => b.classList.remove('selected'));
      tipoSeleccionado = null;
      if (marcador) { mapa.removeLayer(marcador); marcador = null; }
      lat = null; lng = null;
      document.getElementById('btn-abrir-reporte').disabled = true;
      document.getElementById('pin-hint').style.display = '';
      const info = document.getElementById('zona-detectada-info');
      if (info) info.textContent = '';
    }, 2500);

  } catch (ex) {
    // 409 = duplicado detectado → tratar como confirmación, no como error
    if (ex.message && ex.message.startsWith('DUPLICADO:')) {
      const texto = ex.message.split('|').slice(1).join('|');
      heatLayer.addLatLng([lat, lng, 0.5]);
      msgEl.innerHTML = `<i class="bi bi-info-circle me-1"></i>${texto}`;
      msgEl.classList.remove('d-none');
      setTimeout(() => {
        bootstrap.Modal.getInstance(document.getElementById('modalReporte')).hide();
        document.getElementById('reporte-form').reset();
        document.querySelectorAll('.tipo-btn').forEach(b => b.classList.remove('selected'));
        tipoSeleccionado = null;
        if (marcador) { mapa.removeLayer(marcador); marcador = null; }
        lat = null; lng = null;
        document.getElementById('btn-abrir-reporte').disabled = true;
        document.getElementById('pin-hint').style.display = '';
        const info = document.getElementById('zona-detectada-info');
        if (info) info.textContent = '';
      }, 3000);
    } else {
      errEl.textContent = ex.message;
      errEl.classList.remove('d-none');
    }
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-send me-2"></i>Enviar reporte';
  }
});

cargarSelects();

// GPS automático: detecta ubicación actual y abre el modal listo para reportar
function usarUbicacionActual() {
  if (!navigator.geolocation) return;
  navigator.geolocation.getCurrentPosition(pos => {
    lat = pos.coords.latitude;
    lng = pos.coords.longitude;

    document.getElementById('latitud-display').value  = lat.toFixed(6);
    document.getElementById('longitud-display').value = lng.toFixed(6);

    if (marcador) mapa.removeLayer(marcador);
    marcador = L.marker([lat, lng])
      .addTo(mapa)
      .bindPopup('<b>Tu ubicación actual</b>')
      .openPopup();
    mapa.setView([lat, lng], 15);

    const resultado = detectarZona(lat, lng);
    if (resultado) {
      document.getElementById('zona').value = resultado.zona.id_zona;
      mostrarIndicadorZona(resultado);
    }

    const btn = document.getElementById('btn-abrir-reporte');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Reportar aquí';
    document.getElementById('pin-hint').style.display = 'none';

    new bootstrap.Modal(document.getElementById('modalReporte')).show();
  }, () => {}, { enableHighAccuracy: true, timeout: 8000 });
}

// Botón GPS en el header de la página
(function agregarBotonGPS() {
  const header = document.querySelector('.page-header');
  if (!header) return;
  const btn = document.createElement('button');
  btn.className = 'btn btn-scs';
  btn.style.cssText = 'margin-left:.5rem;';
  btn.innerHTML = '<i class="bi bi-geo-alt-fill me-1"></i>Usar mi ubicación';
  btn.onclick = usarUbicacionActual;
  header.appendChild(btn);
})();
