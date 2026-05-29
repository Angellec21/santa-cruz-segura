# Santa Cruz Segura Predictiva

Plataforma web con IA para la anticipación colaborativa del delito en barrios de Santa Cruz, Bolivia.
Permite a vecinos reportar incidentes, a directivos gestionarlos, y predice zonas de riesgo con ML.
El mapa de calor se actualiza en tiempo real mediante WebSockets.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML5 + CSS3 + JavaScript (vanilla) |
| Mapas | Leaflet.js + heatmap.js |
| Gráficas | Chart.js |
| Tiempo real (cliente) | Socket.IO client |
| Backend | Python 3.12 + FastAPI + Uvicorn |
| WebSockets (servidor) | FastAPI WebSocket nativo |
| ORM | SQLAlchemy 2.x + PyMySQL |
| Autenticación | JWT (python-jose) + bcrypt (passlib) |
| Validación | Pydantic v2 |
| Base de datos | MySQL 8 (administrada con MySQL Workbench) |
| IA / ML | scikit-learn + pandas + numpy |
| Entorno | virtualenv — Mac (Apple Silicon / Intel) |

---

## Estructura del proyecto

```
santa-cruz-segura/
├── CLAUDE.md                    ← este archivo
├── requirements.txt
├── .env                         ← variables de entorno (NO subir a git)
├── .env.example
├── .gitignore
│
├── backend/
│   ├── main.py                  ← entrada FastAPI, registro de routers, WebSocket
│   ├── config.py                ← Settings con pydantic-settings
│   ├── database.py              ← engine, SessionLocal, Base
│   │
│   ├── models/                  ← clases SQLAlchemy (una por tabla)
│   │   ├── __init__.py
│   │   ├── junta_vecinal.py
│   │   ├── rol.py
│   │   ├── usuario.py
│   │   ├── tipo_incidente.py
│   │   ├── zona_caliente.py
│   │   ├── reporte.py
│   │   ├── evidencia.py
│   │   ├── alerta.py
│   │   ├── prediccion_ia.py
│   │   ├── notificacion.py
│   │   └── usuario_notificacion.py
│   │
│   ├── schemas/                 ← modelos Pydantic (request / response)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── usuario.py
│   │   ├── reporte.py
│   │   ├── zona.py
│   │   ├── alerta.py
│   │   └── prediccion.py
│   │
│   ├── routers/                 ← un router por dominio
│   │   ├── __init__.py
│   │   ├── auth.py              ← POST /auth/login, /auth/register
│   │   ├── usuarios.py          ← GET /usuarios/me, CRUD admin
│   │   ├── reportes.py          ← POST/GET /reportes, subida evidencia
│   │   ├── zonas.py             ← GET /zonas, heatmap data
│   │   ├── alertas.py           ← GET/POST /alertas
│   │   ├── dashboard.py         ← GET /dashboard/resumen
│   │   └── ia.py                ← POST /ia/predecir/{id_zona}
│   │
│   ├── services/                ← lógica de negocio desacoplada de routers
│   │   ├── auth_service.py
│   │   ├── reporte_service.py
│   │   ├── zona_service.py
│   │   ├── alerta_service.py
│   │   └── ia_service.py        ← carga modelo, predice, guarda prediccion_ia
│   │
│   ├── websocket/
│   │   └── manager.py           ← ConnectionManager: broadcast de eventos al mapa
│   │
│   ├── ml/
│   │   ├── train.py             ← script de entrenamiento (corre aparte)
│   │   ├── model.pkl            ← modelo serializado (gitignored)
│   │   └── predictor.py         ← carga model.pkl y expone predict()
│   │
│   └── utils/
│       ├── security.py          ← hash_password, verify_password, create_token
│       ├── deps.py              ← get_db, get_current_user, require_role
│       └── responses.py         ← helpers de respuesta estándar
│
├── frontend/
│   ├── index.html               ← login / landing
│   ├── dashboard.html           ← panel principal con mapa y métricas
│   ├── reportar.html            ← formulario de reporte ciudadano
│   ├── alertas.html             ← listado de alertas activas
│   ├── admin.html               ← gestión de usuarios y juntas (solo admin)
│   │
│   ├── css/
│   │   ├── base.css             ← reset, variables CSS, tipografía
│   │   ├── components.css       ← botones, cards, badges, formularios
│   │   ├── dashboard.css
│   │   └── mapa.css
│   │
│   ├── js/
│   │   ├── api.js               ← fetch wrapper con JWT header automático
│   │   ├── auth.js              ← login, logout, manejo de token en localStorage
│   │   ├── mapa.js              ← inicializa Leaflet, heatmap, escucha WebSocket
│   │   ├── reportar.js          ← formulario + subida de evidencia
│   │   ├── dashboard.js         ← Chart.js, métricas, v_resumen_barrio
│   │   └── alertas.js
│   │
│   └── assets/
│       ├── logo.svg
│       └── icons/
│
└── database/
    ├── santa_cruz_segura_workbench.sql   ← script completo ya generado (383 líneas)
    └── seeds/
        ├── 01_roles.sql
        ├── 02_juntas.sql
        └── 03_tipos_incidente.sql
```

---

## Base de datos — 11 tablas en 3FN (MySQL 8)

Script listo en `database/santa_cruz_segura_workbench.sql`.

| Tabla | Descripción |
|-------|-------------|
| `junta_vecinal` | Organizaciones vecinales (entidad principal del dominio) |
| `rol` | Catálogo: vecino, directivo, autoridad, admin |
| `usuario` | Usuarios con FK a junta y rol, lat/lng actualizables |
| `tipo_incidente` | Catálogo: Robo, Hurto, Violencia, Sospechoso, Otro |
| `zona_caliente` | Zonas geoespaciales con nivel de riesgo dinámico |
| `reporte` | Reportes ciudadanos con FK a zona, tipo, usuario |
| `evidencia` | Archivos adjuntos a reportes (imagen, video, audio) |
| `alerta` | Alertas preventivas/reactivas por zona |
| `prediccion_ia` | Salida del modelo ML por zona y período |
| `notificacion` | Notificaciones originadas por alertas |
| `usuario_notificacion` | Tabla puente N:N usuario ↔ notificación |

**Trigger activo:** `trg_actualizar_zona_riesgo` — recalcula `nivel_riesgo` en
`zona_caliente` automáticamente tras cada INSERT en `reporte` (últimos 30 días).

**Vista:** `v_resumen_barrio` — usada por el endpoint `/dashboard/resumen`.

---

## Roles y permisos

| Rol | Puede hacer |
|-----|-------------|
| `vecino` | Crear reportes, subir evidencia, ver alertas de su zona |
| `directivo` | Todo lo anterior + validar reportes, emitir alertas, ver dashboard |
| `autoridad` | Ver todas las zonas y juntas, exportar datos |
| `admin` | CRUD completo de usuarios, juntas, configuración global |

Implementado como decorador `require_role(["directivo", "admin"])` en `backend/utils/deps.py`.

---

## Endpoints principales — FastAPI

### Auth
- `POST /auth/login` — retorna JWT access token
- `POST /auth/register` — registro de vecino

### Usuarios
- `GET /usuarios/me` — perfil del usuario autenticado
- `GET /usuarios` — listar (admin)
- `PUT /usuarios/{id}/estado` — activar/suspender (admin)

### Reportes
- `POST /reportes` — crear reporte con lat/lng
- `GET /reportes` — listar con filtros (zona, tipo, estado, fecha)
- `PUT /reportes/{id}/estado` — cambiar estado (directivo)
- `POST /reportes/{id}/evidencia` — subir archivo

### Zonas y mapa
- `GET /zonas` — listado con nivel de riesgo actual
- `GET /zonas/{id}/heatmap` — puntos para heatmap.js
- `WS  /ws/mapa` — WebSocket de tiempo real

### Alertas
- `GET /alertas` — alertas vigentes
- `POST /alertas` — crear alerta manual (directivo)
- `PUT /alertas/{id}/cerrar` — marcar como resuelta

### Dashboard
- `GET /dashboard/resumen` — usa v_resumen_barrio

### IA
- `POST /ia/predecir/{id_zona}` — ejecuta modelo y guarda en prediccion_ia

---

## WebSocket — flujo de tiempo real

```
Vecino reporta (POST /reportes)
  → reporte_service guarda en MySQL
  → trigger MySQL actualiza zona_caliente.nivel_riesgo
  → router llama a manager.broadcast(evento)
  → ConnectionManager emite JSON a todos los WS conectados
  → mapa.js recibe evento → actualiza marcador Leaflet + heatmap
```

Evento JSON emitido por WebSocket:
```json
{
  "tipo": "nuevo_reporte",
  "id_reporte": 42,
  "latitud": -17.7834,
  "longitud": -63.1821,
  "tipo_incidente": "Robo a domicilio",
  "nivel_zona": "alto",
  "id_zona": 3
}
```

---

## Convenciones de código

### Python (backend)
- Nombres de funciones y variables: `snake_case`
- Clases: `PascalCase`
- Schemas Pydantic separados por acción: `ReporteCreate`, `ReporteResponse`, `ReporteUpdate`
- Cada router solo orquesta: la lógica va en el service correspondiente
- Dependencias de DB siempre vía `Depends(get_db)`
- Token JWT siempre via `Depends(get_current_user)`
- Nunca hardcodear strings de roles: usar constantes en `utils/deps.py`

### JavaScript (frontend)
- `api.js` centraliza todos los fetch; nunca hacer fetch directo en otros archivos
- JWT se guarda en `localStorage` bajo la clave `scs_token`
- El mapa Leaflet se inicializa una sola vez en `mapa.js`; otros archivos llaman funciones exportadas
- Nombrar eventos WebSocket con prefijo de dominio: `reporte:nuevo`, `alerta:emitida`

### SQL / Migraciones
- Nunca modificar `santa_cruz_segura_workbench.sql` directamente tras la primera ejecución
- Cambios de schema → nuevo archivo en `database/migrations/` con fecha prefijada: `20260522_agregar_campo_x.sql`

---

## Comandos frecuentes

```bash
# Activar entorno
source venv/bin/activate

# Correr backend en desarrollo
cd backend
uvicorn main:app --reload --port 8000

# Ver docs automáticas de FastAPI
open http://localhost:8000/docs

# Conectar a MySQL desde terminal
mysql -u root -p santa_cruz_segura

# Ejecutar script SQL en Workbench
# File → Open SQL Script → santa_cruz_segura_workbench.sql → Cmd+Shift+Enter

# Entrenar modelo IA (corre aparte, no en uvicorn)
python backend/ml/train.py

# Instalar nuevas dependencias
pip install <paquete> && pip freeze > requirements.txt
```

---

## Variables de entorno (.env)

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=santa_cruz_segura
DB_USER=root
DB_PASSWORD=tu_password

# JWT
SECRET_KEY=cambia_esto_por_una_clave_segura_de_64_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# App
APP_ENV=development
UPLOAD_DIR=uploads/
MAX_UPLOAD_MB=10
```

---

## Lo que NO hacer

- No guardar `model.pkl`, `.env`, `uploads/` en git (ya están en .gitignore)
- No poner lógica de negocio directamente en los routers
- No usar `nivel_riesgo` como campo calculado en `reporte` — se obtiene de `zona_caliente`
- No hacer broadcast de WebSocket sin verificar que el reporte fue guardado exitosamente
- No usar `SELECT *` en queries — especificar columnas siempre en SQLAlchemy

---

## Estado del proyecto

- [x] Modelado conceptual, lógico y físico (3FN)
- [x] Script SQL completo para MySQL Workbench
- [x] Stack tecnológico definido
- [x] Arquitectura de carpetas definida
- [x] CLAUDE.md creado
- [ ] Estructura de carpetas inicializada
- [ ] Modelos SQLAlchemy
- [ ] Auth con JWT
- [ ] CRUD reportes
- [ ] WebSocket + mapa en tiempo real
- [ ] Dashboard con Chart.js
- [ ] Módulo IA predictivo
- [ ] Notificaciones
