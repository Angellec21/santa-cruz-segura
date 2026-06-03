# Santa Cruz Segura Predictiva
## Documentación Técnica Completa

> Plataforma web con IA para la anticipación colaborativa del delito en barrios de Santa Cruz, Bolivia.
> Desarrollada para la materia **Sistemas de Información II — 2026**

---

## Índice

1. [Problema de contexto](#1-problema-de-contexto)
2. [Solución propuesta](#2-solución-propuesta)
3. [Tecnologías utilizadas](#3-tecnologías-utilizadas)
4. [Arquitectura del sistema](#4-arquitectura-del-sistema)
5. [Base de datos](#5-base-de-datos)
6. [Backend — FastAPI](#6-backend--fastapi)
7. [Frontend — Bootstrap 5](#7-frontend--bootstrap-5)
8. [Módulo de Inteligencia Artificial](#8-módulo-de-inteligencia-artificial)
9. [Tiempo real — WebSockets](#9-tiempo-real--websockets)
10. [Seguridad — JWT](#10-seguridad--jwt)
11. [Estado del CRUD por módulo](#11-estado-del-crud-por-módulo)
12. [Conexión API ↔ Formularios](#12-conexión-api--formularios)
13. [Flujo completo del sistema](#13-flujo-completo-del-sistema)
14. [Estructura de carpetas](#14-estructura-de-carpetas)
15. [Historial de desarrollo](#15-historial-de-desarrollo)
16. [Comandos para ejecutar el proyecto](#comandos-para-ejecutar-el-proyecto)

---

## 1. Problema de contexto

En Santa Cruz, Bolivia, las juntas vecinales carecen de sistemas con procesos adecuados de desarrollo y manejo eficiente de bases de datos. Utilizan herramientas improvisadas como **WhatsApp** y **Google Forms**, generando:

| Problema | Consecuencia |
|----------|--------------|
| Información fragmentada entre chats | No hay registro centralizado de incidentes |
| Reportes tardíos e informales | La junta no puede actuar a tiempo |
| Sin análisis histórico | Imposible anticipar patrones delictivos |
| Sin geolocalización exacta | No se sabe dónde ocurren los incidentes realmente |
| Sin sistema de alertas | Los vecinos no son informados preventivamente |

Esto **perpetúa una respuesta reactiva** frente a la inseguridad y profundiza la vulnerabilidad ciudadana, afectando especialmente a mujeres, adultos mayores y niños.

---

## 2. Solución propuesta

**Santa Cruz Segura Predictiva** reemplaza WhatsApp y Google Forms con una plataforma web que:

- Permite a vecinos **reportar incidentes** con ubicación exacta en mapa interactivo
- Centraliza todos los reportes en una **base de datos relacional** (MySQL 8)
- Muestra un **mapa de calor en tiempo real** que se actualiza al instante vía WebSocket
- Usa **Inteligencia Artificial** (Random Forest) para predecir qué zonas escalarán en riesgo
- Emite **alertas preventivas** gestionadas por directivos de junta
- Ofrece un **dashboard** con métricas, gráficas Chart.js y tabla por barrio
- Controla el acceso mediante **roles** (vecino, directivo, autoridad, admin) con JWT

---

## 3. Tecnologías utilizadas

### 3.1 Backend

| Tecnología | Versión | Para qué se usó |
|-----------|---------|-----------------|
| **Python** | 3.9 | Lenguaje principal del servidor |
| **FastAPI** | 0.111 | Framework web para construir la API REST |
| **Uvicorn** | 0.29 | Servidor ASGI que ejecuta FastAPI |
| **SQLAlchemy** | 2.0 | ORM para mapear clases Python a tablas MySQL |
| **PyMySQL** | 1.1 | Driver que conecta SQLAlchemy con MySQL 8 |
| **Pydantic v2** | 2.7 | Validación de datos entrantes y esquemas de respuesta |
| **pydantic-settings** | 2.2 | Lee variables de entorno desde el archivo `.env` |
| **python-jose** | 3.3 | Genera y verifica tokens JWT |
| **passlib + bcrypt** | 1.7 / 4.0.1 | Hashea contraseñas (bcrypt fijado en 4.0.1 por compatibilidad con passlib) |
| **python-multipart** | 0.0.9 | Permite subir archivos de evidencia por formulario |
| **eval-type-backport** | 0.3 | Compatibilidad de tipos modernos (`X \| Y`) en Python 3.9 |

### 3.2 Inteligencia Artificial / Machine Learning

| Tecnología | Versión | Para qué se usó |
|-----------|---------|-----------------|
| **scikit-learn** | 1.4 | Entrenamiento del modelo `RandomForestClassifier` |
| **pandas** | 2.2 | Manipulación de datos para entrenamiento |
| **numpy** | 1.26 | Operaciones numéricas |
| **pickle** | stdlib | Serialización del modelo entrenado a `model.pkl` |

### 3.3 Base de datos

| Tecnología | Versión | Para qué se usó |
|-----------|---------|-----------------|
| **MySQL** | 8.0 | Motor de base de datos relacional principal |
| **MySQL Workbench** | 8.0 | Herramienta visual para ejecutar el script SQL inicial |

### 3.4 Frontend

| Tecnología | Versión | Para qué se usó |
|-----------|---------|-----------------|
| **HTML5** | — | Estructura de todas las páginas |
| **Bootstrap** | 5.3 | Framework CSS: layout, componentes, modales, navbar, sidebar |
| **Bootstrap Icons** | 1.11 | Íconos SVG usados en toda la interfaz |
| **JavaScript** | ES2020 | Lógica del cliente: fetch, DOM, eventos |
| **Leaflet.js** | 1.9 | Mapa interactivo con tiles de OpenStreetMap |
| **leaflet-heat** | 0.2 | Plugin que genera el mapa de calor sobre Leaflet |
| **Chart.js** | 4.4 | Gráfica de dona (reportes por barrio) en el dashboard |
| **WebSocket API** | nativa | Conexión en tiempo real al servidor desde el navegador |

---

## 4. Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────┐
│                      NAVEGADOR                          │
│  HTML5 + Bootstrap 5 + Leaflet + Chart.js + WebSocket   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP REST / WebSocket
┌──────────────────────▼──────────────────────────────────┐
│                   FASTAPI (Python 3.9)                   │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Routers  │  │ Services │  │ Schemas  │  │  Utils │  │
│  │ /auth    │  │ auth     │  │ Pydantic │  │ JWT    │  │
│  │ /usuarios│→ │ reporte  │  │ v2       │  │ bcrypt │  │
│  │ /reportes│  │ zona     │  └──────────┘  └────────┘  │
│  │ /zonas   │  │ alerta   │                             │
│  │ /alertas │  │ ia       │  ┌────────────────────────┐ │
│  │ /dashboard│ └──────────┘  │ WebSocket Manager      │ │
│  │ /ia      │                │ broadcast a clientes   │ │
│  └──────────┘                └────────────────────────┘ │
│        │ Sirve archivos estáticos del frontend           │
│        │ (StaticFiles en /)                              │
└──────────────────────┬──────────────────────────────────┘
                       │ SQLAlchemy ORM + PyMySQL
┌──────────────────────▼──────────────────────────────────┐
│                    MYSQL 8                               │
│  11 tablas + 1 trigger + 1 vista                        │
└─────────────────────────────────────────────────────────┘
```

### Patrón de diseño: Router → Service → Model

Cada petición HTTP sigue este flujo estricto:

```
Request HTTP
    ↓
Router  →  valida con Pydantic, extrae token JWT
    ↓
Service →  lógica de negocio, consultas SQLAlchemy
    ↓
Model   →  mapeo a tabla MySQL
    ↓
Response → serializado por Pydantic (from_attributes=True)
```

Los routers **no** contienen lógica de negocio. Los services **no** conocen de HTTP.

---

## 5. Base de datos

### 5.1 Diagrama de relaciones (11 tablas en 3FN)

```
junta_vecinal ──< usuario >── rol
      │
      ├──< zona_caliente >──< reporte >──< evidencia
      │         │                │
      │         ├──< alerta      └──< tipo_incidente
      │         │      │
      │         │      └──< notificacion >──< usuario_notificacion
      │         │
      │         └──< prediccion_ia
      │
      └──< alerta
```

### 5.2 Descripción de cada tabla

| Tabla | Propósito |
|-------|-----------|
| `junta_vecinal` | Organizaciones vecinales de cada barrio (entidad central del dominio) |
| `rol` | Catálogo de roles: vecino (1), directivo (2), autoridad (3), admin (4) |
| `usuario` | Vecinos y administradores con FK a junta y rol, lat/lng actualizables |
| `tipo_incidente` | Catálogo: Robo domicilio, Robo transeúnte, Hurto, Violencia, Sospechoso, Vandalismo, Otro |
| `zona_caliente` | Zonas geoespaciales con centro, radio y nivel de riesgo dinámico |
| `reporte` | Reportes ciudadanos con lat/lng, tipo, estado y opción de anonimato |
| `evidencia` | Archivos multimedia (imagen, video, audio) adjuntos a un reporte |
| `alerta` | Alertas preventivas/reactivas/informativas emitidas por directivos |
| `prediccion_ia` | Resultados del modelo ML: zona, período, nivel predicho, probabilidad |
| `notificacion` | Notificaciones generadas automáticamente por alertas |
| `usuario_notificacion` | Tabla puente N:N usuario ↔ notificación (registra si fue leída) |

### 5.3 Trigger automático

```sql
-- Se ejecuta DESPUÉS de cada INSERT en la tabla reporte
DELIMITER $$
CREATE TRIGGER trg_actualizar_zona_riesgo
AFTER INSERT ON reporte
FOR EACH ROW
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total
  FROM reporte
  WHERE id_zona = NEW.id_zona
    AND fecha_reporte >= DATE_SUB(NOW(), INTERVAL 30 DAY);

  UPDATE zona_caliente
  SET
    total_reportes_30d = total,
    nivel_riesgo = CASE
      WHEN total >= 20 THEN 'critico'
      WHEN total >= 10 THEN 'alto'
      WHEN total >=  5 THEN 'medio'
      ELSE 'bajo'
    END,
    ultima_actualizacion = NOW()
  WHERE id_zona = NEW.id_zona;
END$$
DELIMITER ;
```

El trigger hace que `nivel_riesgo` **se calcule automáticamente** en MySQL tras cada reporte, sin intervención del backend Python.

### 5.4 Vista para el dashboard

```sql
CREATE VIEW v_resumen_barrio AS
SELECT
  j.nombre        AS junta,
  j.distrito,
  COUNT(DISTINCT u.id_usuario)                         AS total_vecinos,
  COALESCE(SUM(z.total_reportes_30d), 0)              AS reportes_30d,
  COUNT(DISTINCT CASE WHEN a.estado = 'activa' THEN a.id_alerta END) AS alertas_activas,
  COALESCE(MAX(z.nivel_riesgo), 'bajo')               AS nivel_riesgo_max
FROM junta_vecinal j
LEFT JOIN usuario       u ON u.id_junta = j.id_junta
LEFT JOIN zona_caliente z ON z.id_junta = j.id_junta
LEFT JOIN alerta        a ON a.id_junta = j.id_junta
GROUP BY j.id_junta, j.nombre, j.distrito;
```

Usada directamente por el endpoint `GET /dashboard/resumen`.

### 5.5 Datos semilla (seeds)

| Archivo | Contenido |
|---------|-----------|
| `seeds/01_roles.sql` | 4 roles: vecino, directivo, autoridad, admin |
| `seeds/02_juntas.sql` | 5 juntas vecinales de Santa Cruz con coordenadas reales |
| `seeds/03_tipos_incidente.sql` | 7 tipos de incidente con iconos |

Usuario admin creado con el seed: `admin@scs.bo` / `admin123`

---

## 6. Backend — FastAPI

### 6.1 Estructura de archivos

```
backend/
├── main.py          ← Punto de entrada: routers, CORS, StaticFiles, WebSocket
├── config.py        ← Settings (pydantic-settings) que lee el .env
├── database.py      ← engine SQLAlchemy + SessionLocal + Base declarativa
│
├── models/          ← 11 clases ORM (una por tabla MySQL)
│   ├── __init__.py  ← importa y re-exporta todas las clases (necesario para alembic/imports)
│   ├── junta_vecinal.py
│   ├── rol.py
│   ├── usuario.py
│   ├── tipo_incidente.py
│   ├── zona_caliente.py
│   ├── reporte.py
│   ├── evidencia.py
│   ├── alerta.py
│   ├── prediccion_ia.py
│   ├── notificacion.py
│   └── usuario_notificacion.py
│
├── schemas/         ← Pydantic v2: validación de entrada y forma de respuesta
│   ├── auth.py      ← LoginRequest, TokenResponse, RegisterRequest
│   ├── usuario.py   ← UsuarioResponse, UsuarioEstadoUpdate
│   ├── reporte.py   ← ReporteCreate, ReporteResponse, ReporteEstadoUpdate
│   ├── zona.py      ← ZonaResponse, HeatmapPoint
│   ├── alerta.py    ← AlertaCreate, AlertaResponse
│   └── prediccion.py← PrediccionResponse
│
├── routers/         ← 7 routers, uno por dominio (solo orquestan)
│   ├── auth.py
│   ├── usuarios.py
│   ├── reportes.py
│   ├── zonas.py
│   ├── alertas.py
│   ├── dashboard.py
│   └── ia.py
│
├── services/        ← Lógica de negocio separada de los routers
│   ├── auth_service.py
│   ├── reporte_service.py
│   ├── zona_service.py
│   ├── alerta_service.py
│   └── ia_service.py
│
├── websocket/
│   └── manager.py   ← ConnectionManager: lista activa de WS, broadcast()
│
├── ml/
│   ├── train.py     ← Script de entrenamiento (corre aparte, no con uvicorn)
│   ├── predictor.py ← Carga model.pkl y expone predict(); fallback heurístico
│   └── model.pkl    ← Modelo serializado (generado al correr train.py)
│
└── utils/
    ├── security.py  ← hash_password, verify_password, create_access_token, decode_token
    └── deps.py      ← get_db, get_current_user, require_role, constantes de rol
```

### 6.2 Endpoints disponibles

#### Autenticación — sin token requerido

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/auth/login` | Devuelve JWT access token |
| `POST` | `/auth/register` | Registra nuevo vecino (id_rol=1 fijo) |
| `GET`  | `/auth/juntas` | Lista juntas activas (para el dropdown de registro) |
| `GET`  | `/auth/tipos` | Lista tipos de incidente (para el formulario de reporte) |

#### Usuarios — requiere JWT

| Método | Ruta | Rol requerido | Descripción |
|--------|------|---------------|-------------|
| `GET`  | `/usuarios/me` | cualquiera | Perfil del usuario autenticado |
| `GET`  | `/usuarios` | admin | Lista todos los usuarios |
| `PUT`  | `/usuarios/{id}/estado` | admin | Activar o suspender cuenta |

#### Reportes — requiere JWT

| Método | Ruta | Rol requerido | Descripción |
|--------|------|---------------|-------------|
| `POST` | `/reportes` | cualquiera | Crear reporte con lat/lng |
| `GET`  | `/reportes` | cualquiera | Listar con filtros: id_zona, id_tipo, estado |
| `PUT`  | `/reportes/{id}/estado` | directivo/admin | Cambiar estado del reporte |
| `POST` | `/reportes/{id}/evidencia` | cualquiera | Subir archivo multimedia |

#### Zonas y mapa — requiere JWT

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET`  | `/zonas` | Lista zonas con nivel de riesgo actual |
| `GET`  | `/zonas/{id}/heatmap` | Puntos lat/lng + intensidad para leaflet-heat |
| `WS`   | `/ws/mapa` | WebSocket de tiempo real para actualizaciones del mapa |

#### Alertas — requiere JWT

| Método | Ruta | Rol requerido | Descripción |
|--------|------|---------------|-------------|
| `GET`  | `/alertas` | cualquiera | Lista alertas activas |
| `POST` | `/alertas` | directivo/admin | Crear nueva alerta |
| `PUT`  | `/alertas/{id}/cerrar` | directivo/admin | Marcar alerta como resuelta |

#### Dashboard e IA — requiere JWT

| Método | Ruta | Rol requerido | Descripción |
|--------|------|---------------|-------------|
| `GET`  | `/dashboard/resumen` | directivo/admin/autoridad | Datos de v_resumen_barrio |
| `POST` | `/ia/predecir/{id_zona}` | directivo/admin/autoridad | Ejecuta modelo y guarda en prediccion_ia |

### 6.3 Documentación automática de FastAPI

FastAPI genera la documentación interactiva automáticamente:

```
http://localhost:8000/docs   ← Swagger UI (probar endpoints con formularios)
http://localhost:8000/redoc  ← ReDoc (documentación más limpia para leer)
```

---

## 7. Frontend — Bootstrap 5

### 7.1 Páginas

| Archivo | URL | Descripción |
|---------|-----|-------------|
| `index.html` | `/` | Login y registro con tabs (no requiere token) |
| `dashboard.html` | `/dashboard.html` | Panel con sidebar, métricas, mapa de calor, gráfica y tabla |
| `reportar.html` | `/reportar.html` | Mapa a pantalla completa — clic en el mapa abre modal de reporte |
| `alertas.html` | `/alertas.html` | Tarjetas de alertas activas + modal para crear alerta (directivos) |
| `admin.html` | `/admin.html` | Tabla de usuarios + modal activar/suspender (solo admin) |

### 7.2 Archivos JavaScript

| Archivo | Responsabilidad |
|---------|-----------------|
| `api.js` | `fetch` wrapper centralizado — agrega header `Authorization: Bearer {token}` automáticamente. Redirige a login si recibe 401. |
| `auth.js` | Login, registro, logout. `requireAuth(roles)` protege páginas redirigiendo si no hay token o el rol no alcanza. Carga juntas en el dropdown de registro. |
| `mapa.js` | Inicializa Leaflet, dibuja círculos de zonas con color por riesgo, conecta WebSocket. Agrega marcadores y actualiza heatmap en tiempo real. Reconecta el WS cada 5 segundos si se pierde. |
| `dashboard.js` | Carga `/dashboard/resumen`, muestra métricas en cards, renderiza gráfica de dona con Chart.js, llena tabla de barrios con nivel de riesgo. |
| `reportar.js` | Al hacer clic en el mapa captura lat/lng, habilita botón y abre el modal. Carga tipos e incidentes como botones visuales y zonas en dropdown. Envía reporte y evidencia. |
| `alertas.js` | Lista alertas con estilo por tipo (preventiva/reactiva/informativa). Muestra botón "cerrar" solo a directivos/admin. Modal para crear alerta con selects de zona y junta. |

### 7.3 Flujo de autenticación en el frontend

```
1. usuario ingresa email/password en index.html
2. api('/auth/login') → recibe access_token
3. api('/usuarios/me') → recibe datos del perfil
4. localStorage.setItem('scs_token', token)
5. localStorage.setItem('scs_user', JSON.stringify(me))
6. window.location.href = '/dashboard.html'

En cada página protegida:
requireAuth() → si no hay token → redirige a index.html
requireAuth(['admin']) → si rol no coincide → redirige a dashboard.html
```

### 7.4 Componentes Bootstrap usados

- **Modal** — formulario de reporte, nueva alerta, confirmar acción admin
- **Sidebar** fija con navegación principal
- **Cards** con sombra para métricas y alertas
- **Table** con hover para listados de usuarios y barrios
- **Badge** para estados, roles y niveles de riesgo
- **Spinner** en botones mientras se espera respuesta del servidor
- **Alert** para mensajes de error y éxito en formularios
- **Tabs** en index.html para alternar entre login y registro

---

## 8. Módulo de Inteligencia Artificial

### 8.1 Algoritmo: Random Forest Classifier

Se usa `RandomForestClassifier` de scikit-learn para clasificar el nivel de riesgo futuro de una zona en 4 categorías:

| Clase | Etiqueta | Criterio de entrenamiento |
|-------|----------|--------------------------|
| 0 | bajo | < 5 reportes en 30 días |
| 1 | medio | 5 – 9 reportes |
| 2 | alto | 10 – 19 reportes |
| 3 | crítico | ≥ 20 reportes |

### 8.2 Entrenamiento (`backend/ml/train.py`)

```bash
# Correr desde la raíz del proyecto con el venv activo
python backend/ml/train.py
# Genera: backend/ml/model.pkl
# Imprime: Accuracy: 0.9XX
```

El script genera datos sintéticos para el entrenamiento ya que en fase inicial no hay suficientes datos reales. Feature principal: `total_reportes_30d`.

### 8.3 Predicción en producción (`backend/ml/predictor.py`)

El `Predictor` implementa dos modos:

```python
# Modo 1: model.pkl existe → usa el modelo entrenado
nivel, probabilidad = predictor.predict({"total_reportes_30d": 15})
# → ("alto", 0.8200)

# Modo 2 (fallback heurístico): model.pkl no existe
# >= 20 → ("critico", 0.90)
# >= 10 → ("alto",    0.75)
# >=  5 → ("medio",   0.60)
# <   5 → ("bajo",    0.85)
```

### 8.4 Endpoint de predicción

```
POST /ia/predecir/{id_zona}
→ 1. Consulta zona_caliente.total_reportes_30d
→ 2. predictor.predict(features)
→ 3. Guarda resultado en tabla prediccion_ia
→ 4. Retorna: nivel_predicho + probabilidad + período (hoy → hoy+7 días)
```

---

## 9. Tiempo real — WebSockets

### 9.1 Flujo completo

```
1. Vecino hace POST /reportes
2. reporte_service.crear_reporte() guarda en MySQL
3. Trigger MySQL recalcula nivel_riesgo de zona_caliente automáticamente
4. El router llama: await manager.broadcast(evento_json)
5. ConnectionManager itera sobre todos los WebSocket activos y envía
6. Si un WebSocket lanza excepción → se elimina de la lista activa
7. mapa.js recibe el evento JSON
8. agregarMarcador(evento) → nuevo punto en Leaflet
9. heatLayer.addLatLng([lat, lng, 0.9]) → mapa de calor actualizado
```

### 9.2 Estructura del evento WebSocket

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

### 9.3 Reconexión automática del cliente

```javascript
ws.onclose = () => {
  // actualiza badge a "Sin conexión"
  setTimeout(conectarWS, 5000);  // reintenta en 5 segundos
};
```

### 9.4 Indicador visual de estado WS

El `dashboard.html` y `reportar.html` muestran un badge verde "● WS Conectado" o rojo "● Sin conexión WS" según el estado de la conexión en tiempo real.

---

## 10. Seguridad — JWT

### 10.1 Flujo de autenticación

```
1. POST /auth/login  { email, password }
2. Backend verifica bcrypt hash en MySQL (passlib + bcrypt 4.0.1)
3. Genera JWT: payload = { "sub": "id_usuario", "exp": now + 480min }
4. Retorna: { "access_token": "eyJ...", "token_type": "bearer" }
5. Frontend guarda en localStorage["scs_token"]
6. Cada request incluye: Authorization: Bearer eyJ...
7. get_current_user() verifica firma JWT y carga el Usuario desde DB
8. Si el usuario está inactivo (activo=False) → 401
```

### 10.2 Control de roles

```python
# deps.py — constantes de rol
ROL_VECINO    = "vecino"
ROL_DIRECTIVO = "directivo"
ROL_AUTORIDAD = "autoridad"
ROL_ADMIN     = "admin"

# Uso en cualquier endpoint:
@router.post("/alertas")
def crear(
    data: AlertaCreate,
    current_user = Depends(require_role([ROL_DIRECTIVO, ROL_ADMIN]))
):
    ...  # solo llega aquí si el rol coincide
```

### 10.3 Tabla de roles y permisos

| Rol | id_rol | Permisos |
|-----|--------|----------|
| vecino | 1 | Crear reportes, subir evidencia, ver alertas |
| directivo | 2 | + Cambiar estado de reportes, emitir alertas, ver dashboard, predecir IA |
| autoridad | 3 | + Ver todas las zonas, dashboard, predecir IA |
| admin | 4 | Todo lo anterior + CRUD de usuarios |

### 10.4 Almacenamiento de contraseñas

Las contraseñas **nunca** se guardan en texto plano:

```python
# Al registrar:
password_hash = bcrypt.hash("mi_password")  # → "$2b$12$abc..."

# Al hacer login:
bcrypt.verify("mi_password", stored_hash)   # → True / False
```

---

## 11. Estado del CRUD por módulo

### ¿Qué operaciones están implementadas?

| Módulo | Create | Read | Update | Delete |
|--------|:------:|:----:|:------:|:------:|
| **Auth / Registro** | ✅ `POST /auth/register` | — | — | — |
| **Reportes** | ✅ `POST /reportes` | ✅ `GET /reportes` con filtros | ✅ `PUT /reportes/{id}/estado` | ❌ no implementado |
| **Evidencia** | ✅ `POST /reportes/{id}/evidencia` | — | — | ❌ no implementado |
| **Alertas** | ✅ `POST /alertas` | ✅ `GET /alertas` | ✅ `PUT /alertas/{id}/cerrar` | ❌ no implementado |
| **Usuarios** | ✅ vía registro | ✅ `GET /usuarios` | ✅ `PUT /usuarios/{id}/estado` | ❌ no implementado |
| **Zonas** | ❌ solo desde SQL | ✅ `GET /zonas` + heatmap | ❌ solo vía trigger | ❌ no implementado |
| **Dashboard** | — | ✅ `GET /dashboard/resumen` | — | — |
| **Predicción IA** | ✅ `POST /ia/predecir/{id_zona}` | — | — | — |

### Notas sobre el diseño

- El **DELETE** no se implementó intencionalmente: los reportes y alertas deben mantenerse como registro histórico. Los usuarios se "suspenden" en vez de eliminarse.
- Las **zonas** se crean desde MySQL Workbench (son datos geográficos fijos del dominio); el nivel de riesgo lo actualiza el trigger automáticamente.
- El **update de zona** lo realiza el trigger de MySQL — no hay endpoint porque sería redundante.

---

## 12. Conexión API ↔ Formularios

### ¿Cada formulario del frontend llama a su endpoint correspondiente?

| Página | Acción del usuario | Endpoint llamado | Estado |
|--------|-------------------|------------------|--------|
| `index.html` | Formulario de login | `POST /auth/login` | ✅ conectado |
| `index.html` | Dropdown de juntas | `GET /auth/juntas` | ✅ conectado |
| `index.html` | Formulario de registro | `POST /auth/register` | ✅ conectado |
| `dashboard.html` | Carga de métricas | `GET /dashboard/resumen` | ✅ conectado |
| `dashboard.html` | Gráfica de dona | usa datos de `/dashboard/resumen` | ✅ conectado |
| `dashboard.html` | Tabla de barrios | usa datos de `/dashboard/resumen` | ✅ conectado |
| `dashboard.html` | Mapa de calor inicial | `GET /zonas` + `GET /zonas/{id}/heatmap` | ✅ conectado |
| `dashboard.html` | Marcadores en tiempo real | `WS /ws/mapa` | ✅ conectado |
| `reportar.html` | Tipos de incidente | `GET /auth/tipos` | ✅ conectado |
| `reportar.html` | Dropdown de zonas | `GET /zonas` | ✅ conectado |
| `reportar.html` | Enviar reporte | `POST /reportes` | ✅ conectado |
| `reportar.html` | Subir evidencia | `POST /reportes/{id}/evidencia` | ✅ conectado |
| `alertas.html` | Lista de alertas | `GET /alertas` | ✅ conectado |
| `alertas.html` | Dropdown zonas del modal | `GET /zonas` | ✅ conectado |
| `alertas.html` | Dropdown juntas del modal | `GET /auth/juntas` | ✅ conectado |
| `alertas.html` | Crear nueva alerta | `POST /alertas` | ✅ conectado |
| `alertas.html` | Marcar alerta resuelta | `PUT /alertas/{id}/cerrar` | ✅ conectado |
| `admin.html` | Tabla de usuarios | `GET /usuarios` | ✅ conectado |
| `admin.html` | Activar / suspender usuario | `PUT /usuarios/{id}/estado` | ✅ conectado |

### Funcionalidades backend sin UI implementada

| Endpoint | Motivo de ausencia de UI |
|----------|--------------------------|
| `PUT /reportes/{id}/estado` | No hay panel de gestión de reportes para directivos — pendiente |
| `POST /ia/predecir/{id_zona}` | No hay botón en el dashboard para disparar la predicción — pendiente |
| `GET /usuarios/me` | Se usa internamente al hacer login (no hay página de perfil) |

---

## 13. Flujo completo del sistema

### Caso de uso: vecino reporta un robo

```
[Vecino]
  1. Abre http://localhost:8000
  2. Inicia sesión → recibe JWT (válido 8 horas)

  3. Va a "Reportar"
     → Ve el mapa con las zonas dibujadas y sus niveles de riesgo

  4. Hace clic en el lugar exacto donde ocurrió el robo
     → Modal de reporte se abre automáticamente

  5. Selecciona tipo: "Robo a domicilio"
     Selecciona zona, agrega descripción, sube foto
     Clic en "Enviar reporte"

[Backend — FastAPI]
  6. POST /reportes → Pydantic valida los datos
  7. reporte_service.crear_reporte() → INSERT en MySQL
  8. MySQL ejecuta trigger → actualiza nivel_riesgo de zona_caliente
  9. router: await manager.broadcast(evento_json)

[WebSocket — Tiempo real]
  10. ConnectionManager envía JSON a todos los navegadores conectados
  11. mapa.js recibe evento → agregarMarcador(evento)
  12. Nuevo punto aparece en el mapa + heatmap actualizado

[Directivo — en su dashboard]
  13. Ve el nuevo punto aparecer en tiempo real sin recargar
  14. Va a "Alertas" → crea alerta preventiva
  15. Todos los vecinos verán la alerta en su menú

[Módulo IA]
  16. POST /ia/predecir/{id_zona}
  17. predictor.predict({ "total_reportes_30d": N })
  18. Devuelve nivel predicho + probabilidad para próximos 7 días
  19. Resultado guardado en tabla prediccion_ia
```

---

## 14. Estructura de carpetas

```
santa-cruz-segura/
│
├── CLAUDE.md                  ← Contexto del proyecto para Claude Code
├── DOCUMENTACION.md           ← Este archivo
├── requirements.txt           ← Dependencias Python (pip freeze)
├── .env                       ← Variables de entorno (NO subir a git)
├── .env.example               ← Plantilla del .env
├── .gitignore
│
├── backend/
│   ├── main.py                ← Entrada: routers + CORS + StaticFiles + WebSocket /ws/mapa
│   ├── config.py              ← Settings con pydantic-settings (lee .env)
│   ├── database.py            ← engine + SessionLocal + Base declarativa
│   │
│   ├── models/                ← 11 clases ORM (una por tabla MySQL)
│   │   └── __init__.py        ← importa todas las clases (necesario para relaciones ORM)
│   │
│   ├── schemas/               ← Pydantic v2: validación y serialización
│   │   ├── auth.py            ← LoginRequest, TokenResponse, RegisterRequest
│   │   ├── usuario.py         ← UsuarioResponse, UsuarioEstadoUpdate
│   │   ├── reporte.py         ← ReporteCreate, ReporteResponse, ReporteEstadoUpdate
│   │   ├── zona.py            ← ZonaResponse, HeatmapPoint
│   │   ├── alerta.py          ← AlertaCreate, AlertaResponse
│   │   └── prediccion.py      ← PrediccionResponse
│   │
│   ├── routers/               ← 7 routers HTTP (solo orquestan, sin lógica)
│   │   ├── auth.py            ← /auth/login, /auth/register, /auth/juntas, /auth/tipos
│   │   ├── usuarios.py        ← /usuarios/me, /usuarios, /usuarios/{id}/estado
│   │   ├── reportes.py        ← /reportes, /reportes/{id}/estado, /reportes/{id}/evidencia
│   │   ├── zonas.py           ← /zonas, /zonas/{id}/heatmap
│   │   ├── alertas.py         ← /alertas, /alertas/{id}/cerrar
│   │   ├── dashboard.py       ← /dashboard/resumen
│   │   └── ia.py              ← /ia/predecir/{id_zona}
│   │
│   ├── services/              ← Lógica de negocio desacoplada
│   │   ├── auth_service.py    ← login(), register()
│   │   ├── reporte_service.py ← crear_reporte(), listar_reportes(), actualizar_estado(), guardar_evidencia()
│   │   ├── zona_service.py    ← listar_zonas(), heatmap_zona()
│   │   ├── alerta_service.py  ← listar_alertas(), crear_alerta(), cerrar_alerta()
│   │   └── ia_service.py      ← predecir_zona()
│   │
│   ├── websocket/
│   │   └── manager.py         ← ConnectionManager: connect(), disconnect(), broadcast()
│   │
│   ├── ml/
│   │   ├── train.py           ← Entrenamiento offline (genera model.pkl)
│   │   ├── predictor.py       ← Carga model.pkl + fallback heurístico
│   │   └── model.pkl          ← Modelo serializado (gitignored, generado al correr train.py)
│   │
│   └── utils/
│       ├── security.py        ← hash_password, verify_password, create_access_token, decode_token
│       └── deps.py            ← get_db, get_current_user, require_role, constantes ROL_*
│
├── frontend/
│   ├── index.html             ← Login / Registro (tabs Bootstrap)
│   ├── dashboard.html         ← Métricas + mapa de calor + gráfica + tabla
│   ├── reportar.html          ← Mapa interactivo + modal de reporte
│   ├── alertas.html           ← Listado de alertas + modal nueva alerta
│   ├── admin.html             ← Gestión de usuarios (solo admin)
│   │
│   ├── css/
│   │   ├── base.css           ← Variables CSS, reset
│   │   ├── components.css     ← Botones, cards, badges personalizados
│   │   ├── dashboard.css      ← Layout del dashboard
│   │   └── mapa.css           ← Estilos específicos del mapa
│   │
│   └── js/
│       ├── api.js             ← fetch wrapper + manejo automático de JWT + logout en 401
│       ├── auth.js            ← Login, registro, requireAuth(), cargarJuntas()
│       ├── mapa.js            ← Leaflet, heatmap, WebSocket, marcadores
│       ├── dashboard.js       ← Métricas, Chart.js, tabla de barrios
│       ├── reportar.js        ← Click en mapa, modal, envío de reporte + evidencia
│       └── alertas.js         ← Lista, crear, cerrar alertas
│
├── database/
│   ├── santa_cruz_segura_workbench.sql  ← Script completo: tablas + trigger + vista + seeds
│   └── seeds/
│       ├── 01_roles.sql                 ← 4 roles del sistema
│       ├── 02_juntas.sql                ← 5 juntas vecinales con coordenadas
│       └── 03_tipos_incidente.sql       ← 7 tipos de incidente
│
└── uploads/                   ← Evidencias subidas por vecinos (gitignored)
```

---

## 15. Historial de desarrollo

### Sesión 1 — Diseño y modelado
- Levantamiento del problema: reemplazar WhatsApp/Google Forms en juntas vecinales de Santa Cruz
- Modelado conceptual, lógico y físico de la base de datos (11 tablas en 3FN)
- Definición del stack tecnológico: FastAPI + MySQL + Bootstrap + Leaflet
- Diseño del trigger `trg_actualizar_zona_riesgo` y la vista `v_resumen_barrio`
- Creación del script SQL completo (`santa_cruz_segura_workbench.sql`, 383 líneas)
- Creación de `CLAUDE.md` con la arquitectura completa del proyecto

### Sesión 2 — Backend completo
- Inicialización de la estructura de carpetas del proyecto
- Configuración del entorno virtual Python 3.9 con `venv`
- Instalación de dependencias: FastAPI, SQLAlchemy, PyMySQL, python-jose, passlib, etc.
- Resolución de compatibilidad: `bcrypt` fijado en 4.0.1 (passlib no soporta 5.x), `eval-type-backport` para tipos modernos en Python 3.9
- Implementación de todos los modelos SQLAlchemy (11 clases ORM)
- Implementación de todos los schemas Pydantic v2
- Implementación de los 7 routers FastAPI
- Implementación de los 5 services con lógica de negocio
- Implementación de `ConnectionManager` para WebSocket broadcast
- Implementación del módulo IA: `predictor.py` con fallback heurístico + `train.py`
- Implementación de `utils/security.py` (JWT + bcrypt) y `utils/deps.py` (dependencias FastAPI)
- Configuración de CORS, StaticFiles y WebSocket en `main.py`
- Ejecución del script SQL en MySQL Workbench y carga de seeds
- Creación del usuario admin: `admin@scs.bo` / `admin123`
- Verificación de la API en `http://localhost:8000/docs`

### Sesión 3 — Frontend completo
- Implementación de las 5 páginas HTML con Bootstrap 5 y Bootstrap Icons
- `index.html`: login con tabs, formulario de registro, carga dinámica de juntas
- `dashboard.html`: sidebar, 4 cards de métricas, mapa Leaflet con heatmap, gráfica Chart.js, tabla de barrios
- `reportar.html`: mapa a pantalla completa, click → modal de reporte, botones visuales de tipo incidente, subida de evidencia
- `alertas.html`: tarjetas por tipo (preventiva/reactiva/informativa), modal nueva alerta con selects dinámicos
- `admin.html`: tabla de usuarios con activar/suspender, modal de confirmación
- Implementación de `api.js`, `auth.js`, `mapa.js`, `dashboard.js`, `reportar.js`, `alertas.js`
- Conexión de todos los formularios a sus endpoints correspondientes
- `DOCUMENTACION.md` técnica completa del proyecto

### Sesión 4 — Limpieza de código
- Eliminado `backend/utils/responses.py` (archivo completo sin usar)
- Eliminada clase `HeatmapResponse` de `schemas/zona.py` (nunca referenciada)
- Eliminada clase `UsuarioUpdate` de `schemas/usuario.py` (sin endpoint que la use)
- Eliminado import `from backend.models.rol import Rol` de `auth_service.py`
- Eliminado import `String` sin usar de `models/reporte.py`
- Eliminado import `Boolean` sin usar de `models/alerta.py`
- Eliminado import `JWTError` sin usar de `utils/security.py`
- Movido `from fastapi import HTTPException` al nivel de módulo en `routers/usuarios.py` (estaba dentro del cuerpo de función)
- Actualización de `DOCUMENTACION.md` con estado real del CRUD y la conexión API↔formularios

---

## Comandos para ejecutar el proyecto

```bash
# 1. Ir al directorio del proyecto
cd "/Users/angelemanuellecaroquispe/Documents/Sistemas de informacion ll/santa-cruz-segura"

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Iniciar el servidor
uvicorn backend.main:app --reload --port 8000

# 4. Abrir en el navegador
open http://localhost:8000

# 5. Ver documentación interactiva de la API
open http://localhost:8000/docs

# 6. Entrenar el modelo IA (opcional — ya funciona con heurística)
python backend/ml/train.py

# 7. Conectar a MySQL directamente
mysql -u root santa_cruz_segura
```

## Variables de entorno (`.env`)

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=santa_cruz_segura
DB_USER=root
DB_PASSWORD=              # sin password en desarrollo local

# JWT
SECRET_KEY=cambia_esto_por_una_clave_segura_de_64_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# App
APP_ENV=development
UPLOAD_DIR=uploads/
MAX_UPLOAD_MB=10
```

## Credenciales del sistema

| Usuario | Email | Password | Rol |
|---------|-------|----------|-----|
| Admin Sistema | admin@scs.bo | admin123 | admin (id_rol=4) |

---

## Estado actual del proyecto

| Módulo | Estado |
|--------|--------|
| Base de datos MySQL (11 tablas + trigger + vista) | ✅ Completo |
| Seeds (roles, juntas, tipos, admin) | ✅ Cargados |
| Backend FastAPI (modelos, schemas, routers, services) | ✅ Completo |
| Autenticación JWT + bcrypt | ✅ Funcionando |
| WebSocket tiempo real | ✅ Funcionando |
| Frontend Bootstrap 5 (5 páginas) | ✅ Completo |
| Formularios conectados a la API | ✅ Todos conectados |
| Módulo IA con fallback heurístico | ✅ Funcionando |
| Modelo ML entrenado (model.pkl) | ⏳ Pendiente (usar `python backend/ml/train.py`) |
| UI para gestionar estado de reportes (directivos) | ⏳ Pendiente |
| UI para disparar predicción IA por zona | ⏳ Pendiente |

---

*Desarrollado para la materia Sistemas de Información II — Santa Cruz, Bolivia, 2026*
