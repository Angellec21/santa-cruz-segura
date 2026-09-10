requireAuth();

const SANTA_CRUZ_CENTER = [-17.7834, -63.1821];
const COLOR_RIESGO  = { bajo: '#22c55e', medio: '#eab308', alto: '#ef4444', critico: '#b91c1c' };
const FILL_OP       = { bajo: 0.35,    medio: 0.50,    alto: 0.65,    critico: 0.80 };
const LABEL_COLOR   = { bajo: '#22c55e', medio: '#eab308', alto: '#ef4444', critico: '#ff4444' };
const COLOR_REPORTE = '#f43f5e'; // color fijo para marcadores de reportes individuales

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
    fillOpacity: fo, weight: 2.5, opacity: 1,
  }).bindPopup(
    `<b>${nombre}</b><br>` +
    `Riesgo: <b style="color:${label}">${nivel.toUpperCase()}</b><br>` +
    `Reportes 30d: <b>${reportes30d}</b>`
  ).addTo(map);

  // Núcleo central brillante
  L.circle([lat, lng], {
    radius: radio * 0.38,
    color: 'transparent', fillColor: color,
    fillOpacity: Math.min(fo * 1.3, 0.95), weight: 0,
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
let marcadoresReportes = null;
let zonasMap    = {};
let tiposMap    = {};

function initMapa(elementId = 'mapa') {
  mapaLeaflet = L.map(elementId, { zoomControl: false }).setView(SANTA_CRUZ_CENTER, 13);
  L.control.zoom({ position: 'bottomright' }).addTo(mapaLeaflet);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap', maxZoom: 19,
  }).addTo(mapaLeaflet);
  heatLayer = L.heatLayer([], { radius: 35, blur: 25, maxZoom: 17, gradient: { 0.3:'#7c3aed', 0.6:'#00d47a', 0.8:'#f59e0b', 1.0:'#ef4444' } }).addTo(mapaLeaflet);
  marcadoresReportes = L.layerGroup().addTo(mapaLeaflet);
  cargarMapa();
  conectarWebSocket();
  // Respaldo por si el WebSocket se corta (ej. el free tier de Render duerme el proceso)
  setInterval(cargarReportesExistentes, 30000);
}

// Actualización en tiempo real: el backend emite "nuevo_reporte" apenas se guarda
// un reporte y la zona recalcula su riesgo (ver backend/services/reporte_service.py)
function marcarEstadoWS(conectado) {
  const badge = document.getElementById('ws-badge-map');
  if (!badge) return;
  badge.className = 'ws-pill ' + (conectado ? 'on' : 'off');
  badge.innerHTML = `<span class="ws-dot"></span>${conectado ? 'En línea' : 'Sin conexión'}`;
}

function conectarWebSocket() {
  const protocolo = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocolo}//${location.host}/ws/mapa`);

  ws.onopen = () => marcarEstadoWS(true);

  ws.onmessage = (evento) => {
    const data = JSON.parse(evento.data);
    if (data.tipo === 'nuevo_reporte') {
      cargarReportesExistentes();
    }
  };

  ws.onclose = () => {
    marcarEstadoWS(false);
    setTimeout(conectarWebSocket, 5000);
  };
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
    const [reportes, heatPuntos] = await Promise.all([
      api('/reportes'),
      api('/zonas/heatmap/all'),
    ]);

    const puntos = heatPuntos.map(p => [p.lat, p.lng, p.intensity]);
    heatLayer.setLatLngs(puntos);

    marcadoresReportes.clearLayers();
    reportes.forEach(r => {
      const tipoNombre = tiposMap[r.id_tipo] || 'Incidente';
      const fecha     = new Date(r.fecha_reporte).toLocaleDateString('es-BO', { day: '2-digit', month: 'short', year: 'numeric' });
      const hora      = new Date(r.fecha_reporte).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' });

      // Color fijo: un reporte siempre se ve, sin importar el riesgo agregado de la zona
      const color = COLOR_REPORTE;
      const icon = L.divIcon({
        className: '',
        html: `<div style="
          width:14px;height:14px;border-radius:50%;
          background:${color};border:2px solid rgba(255,255,255,.9);
          box-shadow:0 0 8px ${color},0 0 2px rgba(0,0,0,.8);
        "></div>`,
        iconAnchor: [7, 7],
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
        .addTo(marcadoresReportes);
    });
  } catch (e) { console.error('Error cargando reportes:', e); }
}


window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('mapa')) initMapa('mapa');
});
