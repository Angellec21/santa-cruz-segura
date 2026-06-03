requireAuth();

const SANTA_CRUZ_CENTER = [-17.7834, -63.1821];
const COLOR_RIESGO  = { bajo: '#22c55e', medio: '#eab308', alto: '#ef4444', critico: '#b91c1c' };
const FILL_OP       = { bajo: 0.13,    medio: 0.22,    alto: 0.32,    critico: 0.42 };
const LABEL_COLOR   = { bajo: '#22c55e', medio: '#eab308', alto: '#ef4444', critico: '#ff4444' };

function dibujarZonaCalor(map, lat, lng, radio, nivel, nombre, reportes30d) {
  const color  = COLOR_RIESGO[nivel] || '#22c55e';
  const fo     = FILL_OP[nivel]     || 0.13;
  const label  = LABEL_COLOR[nivel] || '#22c55e';

  // Halo exterior (desvanecido)
  L.circle([lat, lng], {
    radius: radio * 1.12,
    color: color, fillColor: color,
    fillOpacity: fo * 0.35, weight: 0, opacity: 0,
    interactive: false,
  }).addTo(map);

  // Círculo principal con borde
  L.circle([lat, lng], {
    radius: radio,
    color: color, fillColor: color,
    fillOpacity: fo, weight: 1.8, opacity: 0.8,
  }).bindPopup(
    `<b>${nombre}</b><br>` +
    `Riesgo: <b style="color:${label}">${nivel.toUpperCase()}</b><br>` +
    `Reportes 30d: <b>${reportes30d}</b>`
  ).addTo(map);

  // Núcleo central brillante
  L.circle([lat, lng], {
    radius: radio * 0.38,
    color: 'transparent', fillColor: color,
    fillOpacity: Math.min(fo * 2.8, 0.75), weight: 0,
    interactive: false,
  }).addTo(map);

  // Etiqueta de zona
  L.marker([lat, lng], {
    icon: L.divIcon({
      className: '',
      html: `<div style="
        background:rgba(6,14,10,.82);color:${label};
        font-size:.62rem;font-weight:700;
        padding:.18rem .48rem;border-radius:8px;
        white-space:nowrap;border:1px solid ${color}44;
        box-shadow:0 0 8px ${color}44;
        backdrop-filter:blur(4px);
      ">${nombre}</div>`,
      iconAnchor: [0, 0],
    }),
    interactive: false, keyboard: false,
  }).addTo(map);
}

let mapaLeaflet = null;
let heatLayer   = null;
let ws          = null;
let zonasMap    = {};   // id_zona → objeto zona (para cruzar nivel_riesgo al recibir WS)
let tiposMap    = {};   // id_tipo → nombre (para mostrar en popup de reportes históricos)

function initMapa(elementId = 'mapa') {
  mapaLeaflet = L.map(elementId, { zoomControl: false }).setView(SANTA_CRUZ_CENTER, 13);
  L.control.zoom({ position: 'bottomright' }).addTo(mapaLeaflet);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO', maxZoom: 19,
  }).addTo(mapaLeaflet);
  heatLayer = L.heatLayer([], { radius: 35, blur: 25, maxZoom: 17, gradient: { 0.3:'#7c3aed', 0.6:'#00d47a', 0.8:'#f59e0b', 1.0:'#ef4444' } }).addTo(mapaLeaflet);
  conectarWS();
  cargarMapa();
}

// Carga zonas, heatmap Y reportes existentes como marcadores
async function cargarMapa() {
  try {
    // 1. Tipos, zonas, heatmap global y reportes — todo en paralelo (3 requests en vez de 12)
    const [tipos, zonas, heatPuntos] = await Promise.all([
      fetch('/auth/tipos').then(r => r.json()),
      api('/zonas'),
      api('/zonas/heatmap/all'),
    ]);
    tipos.forEach(t => { tiposMap[t.id_tipo] = t.nombre; });

    // 2. Dibujar zonas y cargar reportes en paralelo
    zonas.forEach(zona => {
      zonasMap[zona.id_zona] = zona;
      dibujarZonaCalor(
        mapaLeaflet,
        parseFloat(zona.latitud_centro), parseFloat(zona.longitud_centro),
        zona.radio_metros, zona.nivel_riesgo, zona.nombre, zona.total_reportes_30d
      );
    });

    // 3. Heatmap con datos ya recibidos + reportes en paralelo
    const puntos = heatPuntos.map(p => [p.lat, p.lng, p.intensity]);
    if (puntos.length) heatLayer.setLatLngs(puntos);

    await cargarReportesExistentes();

  } catch (e) { console.error('Error cargando mapa:', e); }
}

async function cargarReportesExistentes() {
  try {
    const reportes = await api('/reportes');
    reportes.forEach(r => {
      const zona      = zonasMap[r.id_zona];
      const nivel     = zona ? zona.nivel_riesgo : 'bajo';
      const tipoNombre = tiposMap[r.id_tipo] || 'Incidente';
      const fecha     = new Date(r.fecha_reporte).toLocaleDateString('es-BO', { day: '2-digit', month: 'short', year: 'numeric' });
      const hora      = new Date(r.fecha_reporte).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' });

      const color = COLOR_RIESGO[nivel] || '#94a3b8';
      const icon = L.divIcon({
        className: '',
        html: `<div style="
          width:12px;height:12px;border-radius:50%;
          background:${color};border:2px solid rgba(255,255,255,.9);
          box-shadow:0 0 8px ${color},0 0 2px rgba(0,0,0,.8);
        "></div>`,
        iconAnchor: [6, 6],
      });

      const estadoBadge = {
        pendiente:  '<span style="color:#fbbf24">● Pendiente</span>',
        verificado: '<span style="color:#60a5fa">● Verificado</span>',
        resuelto:   '<span style="color:#34d399">● Resuelto</span>',
        descartado: '<span style="color:#64748b">● Descartado</span>',
      }[r.estado] || r.estado;

      L.marker([parseFloat(r.latitud), parseFloat(r.longitud)], { icon })
        .bindPopup(
          `<b>${tipoNombre}</b><br>` +
          `${estadoBadge}<br>` +
          `<small style="color:#94a3b8">${fecha} ${hora}</small>` +
          (r.descripcion ? `<br><small style="color:#64748b">${r.descripcion}</small>` : '')
        )
        .addTo(mapaLeaflet);
    });
  } catch (e) { console.error('Error cargando reportes:', e); }
}

function conectarWS() {
  const wsProto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new WebSocket(`${wsProto}//${window.location.host}/ws/mapa`);
  const dot = '<i class="bi bi-circle-fill" style="font-size:.38rem"></i>';

  function setWsBadge(on) {
    const text = on ? 'En vivo' : 'Sin conexión';
    const cls  = on ? 'ws-pill on' : 'ws-pill off';
    ['ws-badge-map','ws-badge','ws-status'].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      el.className = cls;
      el.innerHTML = `${dot} ${text}`;
    });
  }

  ws.onopen    = () => setWsBadge(true);
  ws.onclose   = () => { setWsBadge(false); setTimeout(conectarWS, 5000); };
  ws.onmessage = e => {
    const evento = JSON.parse(e.data);
    if (evento.tipo === 'nuevo_reporte') agregarMarcadorNuevo(evento);
  };
}

// Marcador para reportes nuevos llegados por WebSocket (más grande, animado)
function agregarMarcadorNuevo(evento) {
  const color = COLOR_RIESGO[evento.nivel_zona] || '#00d47a';
  const icon = L.divIcon({
    className: '',
    html: `<div style="position:relative;width:20px;height:20px">
      <div style="
        position:absolute;inset:0;border-radius:50%;
        background:${color};opacity:.25;
        animation:ws-ring 1.5s ease-out infinite;
      "></div>
      <div style="
        position:absolute;inset:4px;border-radius:50%;
        background:${color};border:2px solid rgba(255,255,255,.9);
        box-shadow:0 0 12px ${color};
      "></div>
    </div>
    <style>
      @keyframes ws-ring{0%{transform:scale(1);opacity:.4}100%{transform:scale(2.5);opacity:0}}
    </style>`,
    iconAnchor: [10, 10],
  });

  const hora = new Date().toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' });

  L.marker([evento.latitud, evento.longitud], { icon })
    .bindPopup(
      `<b>${evento.tipo_incidente}</b><br>` +
      `<span style="color:#fbbf24">● Nuevo reporte</span><br>` +
      `<small style="color:#94a3b8">Riesgo <b style="color:${color}">${evento.nivel_zona}</b> · ${hora}</small>`
    )
    .addTo(mapaLeaflet)
    .openPopup();

  heatLayer.addLatLng([evento.latitud, evento.longitud, 0.9]);

  // Actualizar el círculo de zona si está en el mapa
  const zona = zonasMap[evento.id_zona];
  if (zona) zona.nivel_riesgo = evento.nivel_zona;
}

window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('mapa')) initMapa('mapa');
});
