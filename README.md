```markdown
<img src="frontend/assets/logo.svg" width="60" height="60" alt="SCS Logo">

# Santa Cruz Segura Predictiva

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://mysql.com)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-199900?logo=leaflet)](https://leafletjs.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.6.1-F7931E?logo=scikit-learn)](https://scikit-learn.org)
[![Railway](https://img.shields.io/badge/Railway-Deployed-0B0D0E?logo=railway)](https://railway.com)

**Plataforma colaborativa de predicción del delito para Santa Cruz de la Sierra, Bolivia**

[📚 Documentación completa del proyecto](https://drive.google.com/drive/folders/1HXZqqYPVU5HvbYCr5LiGRrGLIiw-v56L?usp=sharing)

</div>

---

## 📌 Índice

- [Descripción General](#descripción-general)
- [Características Principales](#características-principales)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución Local](#ejecución-local)
- [Despliegue en Railway](#despliegue-en-railway)
- [Base de Datos](#base-de-datos)
- [Endpoints de la API](#endpoints-de-la-api)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [WebSockets en Tiempo Real](#websockets-en-tiempo-real)
- [Roles y Permisos](#roles-y-permisos)
- [Manual de Usuario](#manual-de-usuario)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Contacto](#contacto)

---

## 📖 Descripción General

**Santa Cruz Segura Predictiva** es una plataforma web integral diseñada para abordar los desafíos de seguridad ciudadana en Santa Cruz de la Sierra, Bolivia. El sistema combina reportes ciudadanos, mapas interactivos, inteligencia artificial y comunicación en tiempo real para crear una herramienta colaborativa que permite anticipar incidentes delictivos.

Los vecinos pueden reportar incidentes directamente desde el mapa, los directivos de juntas vecinales pueden gestionar alertas preventivas y reactivas, las autoridades visualizan patrones de riesgo, y todo el sistema se apoya en un modelo de machine learning que predice el nivel de riesgo de cada zona para los próximos siete días.

---

## ⭐ Características Principales

| Área | Funcionalidad |
|------|---------------|
| **Autenticación** | Registro e inicio de sesión con JWT, recuperación de contraseña (próximamente) |
| **Roles de usuario** | Vecino, Directivo, Autoridad, Administrador con permisos diferenciados |
| **Mapa interactivo** | Visualización de zonas calientes, círculos de riesgo, mapa de calor |
| **Reportes** | Creación de incidentes con geolocalización, evidencias (imagen/video/audio) y opción anónima |
| **Alertas** | Emisión y gestión de alertas preventivas, reactivas e informativas |
| **IA Predictiva** | Predicción de nivel de riesgo (bajo/medio/alto/crítico) para los próximos 7 días |
| **Tiempo real** | WebSockets que actualizan el mapa instantáneamente al crear un reporte |
| **Dashboard** | Métricas, gráficas de tendencia, resumen por barrio |
| **Panel admin** | Gestión de usuarios, cambio de roles, activación/suspensión de cuentas |

---

## 🛠️ Tecnologías Utilizadas

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|------------|
| **FastAPI** | 0.111.0 | Framework web principal, alto rendimiento y documentación automática |
| **Uvicorn** | 0.29.0 | Servidor ASGI para ejecutar FastAPI |
| **SQLAlchemy** | 2.0.30 | ORM para mapeo objeto-relacional |
| **PyMySQL** | 1.1.0 | Conector MySQL para Python |
| **Python-JOSE** | 3.3.0 | Creación y verificación de tokens JWT |
| **bcrypt** | 4.2.1 | Hashing seguro de contraseñas |
| **Pydantic** | 2.7.1 | Validación de datos y configuración |
| **Python-Multipart** | 0.0.9 | Manejo de subida de archivos |

### Machine Learning
| Tecnología | Versión | Propósito |
|------------|---------|------------|
| **Scikit-learn** | 1.6.1 | Algoritmo Random Forest Classifier |
| **NumPy** | 2.2.6 | Generación de datos sintéticos |
| **Pandas** | 2.2.3 | Manipulación opcional de datos |

### Frontend
| Tecnología | Versión | Propósito |
|------------|---------|------------|
| **HTML5 + CSS3** | - | Estructura y estilos base |
| **Bootstrap 5** | 5.3.3 | Componentes responsivos |
| **Bootstrap Icons** | 1.11.3 | Biblioteca de iconos |
| **Leaflet** | 1.9.4 | Mapas interactivos |
| **Leaflet.heat** | 0.2.0 | Plugin para mapa de calor |
| **Chart.js** | 4.4.2 | Gráficas de tendencia y tipos |
| **Fetch API** | - | Peticiones HTTP asíncronas |
| **WebSocket API** | - | Comunicación en tiempo real |

### Base de Datos
| Tecnología | Versión | Propósito |
|------------|---------|------------|
| **MySQL** | 8.0 | Motor de base de datos relacional |
| **Triggers** | - | Actualización automática del nivel de riesgo |
| **Views** | - | Vista materializada para resúmenes |

### Despliegue
| Tecnología | Versión | Propósito |
|------------|---------|------------|
| **Railway** | - | Plataforma de despliegue en la nube |
| **Nixpacks** | - | Builder para entornos Python |
| **Git** | - | Control de versiones |

---

## 🏗️ Arquitectura del Sistema

La arquitectura sigue un modelo cliente-servidor de tres capas:

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTE                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    HTML5    │  │    CSS3     │  │  JavaScript (ES6)   │  │
│  │  Bootstrap  │  │   Leaflet   │  │  WebSocket API      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                    HTTP + WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       SERVIDOR (FastAPI)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                     ROUTERS                             │  │
│  │  /auth  /usuarios  /reportes  /zonas  /alertas  /ia   │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    SERVICES                             │  │
│  │  Auth  |  Reporte  |  Zona  |  Alerta  |  IA           │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   ML Model   │  │  WebSocket   │  │   Middleware     │  │
│  │ RandomForest │  │   Manager    │  │   (CORS, Auth)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                         SQLAlchemy ORM
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   BASE DE DATOS (MySQL)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  usuario | rol | junta_vecinal | zona_caliente        │  │
│  │  tipo_incidente | reporte | evidencia | alerta        │  │
│  │  notificacion | usuario_notificacion | prediccion_ia  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌──────────────┐  ┌──────────────────────────────────────┐  │
│  │   Triggers   │  │               Views                   │  │
│  │ trg_actualizar│  │ v_resumen_barrio                     │  │
│  └──────────────┘  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Flujos principales:

1. **Reporte de incidente**: Usuario → Frontend → API → Base de datos → WebSocket → Todos los clientes conectados
2. **Predicción IA**: Directivo → API → Predictor (Random Forest) → Base de datos → Frontend
3. **Autenticación**: Frontend → API → Validación bcrypt → Generación JWT → Frontend

---

## 📁 Estructura del Proyecto

```
santa-cruz-segura/
│
├── backend/                      # Backend FastAPI
│   ├── ml/                       # Módulo de Machine Learning
│   │   ├── predictor.py          # Clase Predictor con carga del modelo
│   │   └── train.py              # Entrenamiento del Random Forest
│   ├── models/                   # Modelos SQLAlchemy (11 tablas)
│   │   ├── usuario.py
│   │   ├── reporte.py
│   │   ├── zona_caliente.py
│   │   ├── alerta.py
│   │   └── ... (otros modelos)
│   ├── routers/                  # Endpoints de la API
│   │   ├── auth.py               # /auth/login, /auth/register
│   │   ├── usuarios.py           # /usuarios/me, /usuarios (admin)
│   │   ├── reportes.py           # /reportes, /reportes/gestion
│   │   ├── zonas.py              # /zonas, /zonas/{id}/heatmap
│   │   ├── alertas.py            # /alertas, /alertas/{id}/cerrar
│   │   ├── dashboard.py          # /dashboard/resumen, tendencia, tipos
│   │   └── ia.py                 # /ia/predecir/{id}, /ia/predicciones
│   ├── schemas/                  # Esquemas Pydantic
│   │   ├── usuario.py
│   │   ├── reporte.py
│   │   ├── auth.py
│   │   └── ...
│   ├── services/                 # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── reporte_service.py
│   │   ├── ia_service.py
│   │   └── ...
│   ├── utils/                    # Utilidades
│   │   ├── deps.py               # Dependencias (get_db, get_current_user)
│   │   └── security.py           # Hash, JWT
│   ├── websocket/                # WebSocket Manager
│   │   └── manager.py
│   ├── config.py                 # Configuración con Pydantic Settings
│   ├── database.py               # Conexión MySQL con SQLAlchemy
│   └── main.py                   # Punto de entrada FastAPI
│
├── frontend/                     # Frontend HTML/JS/CSS
│   ├── js/                       # Módulos JavaScript
│   │   ├── api.js                # Peticiones HTTP con token
│   │   ├── auth.js               # Autenticación y sidebar
│   │   ├── mapa.js               # Inicialización Leaflet + WebSocket
│   │   ├── dashboard.js          # Métricas y gráficas Chart.js
│   │   ├── alertas.js            # Gestión de alertas
│   │   └── reportar.js           # Reporte con mapa interactivo
│   ├── css/                      # Estilos adicionales
│   │   └── animations.css
│   ├── assets/                   # Recursos estáticos
│   │   ├── logo.svg
│   │   └── favicon.svg
│   ├── index.html                # Página de login/registro
│   ├── dashboard.html            # Dashboard principal
│   ├── reportar.html             # Reporte de incidentes
│   ├── mis-reportes.html         # Reportes del usuario
│   ├── gestionar-reportes.html   # Gestión (directivos/admin)
│   ├── alertas.html              # Listado de alertas
│   └── admin.html                # Panel de administración
│
├── uploads/                      # Directorio de evidencias (creado automáticamente)
├── .env.example                  # Ejemplo de variables de entorno
├── .gitignore                    # Archivos ignorados por git
├── requirements.txt              # Dependencias Python
├── railway.json                  # Configuración de despliegue Railway
└── README.md                     # Este archivo
```

---

## 📋 Requisitos Previos

| Requisito | Versión | Notas |
|-----------|---------|-------|
| **Python** | 3.9+ | Lenguaje principal del backend |
| **MySQL** | 8.0+ | Base de datos relacional |
| **pip** | Última versión | Gestor de paquetes Python |
| **Git** | 2.x+ | Control de versiones (opcional) |
| **Navegador** | Moderno | Chrome, Firefox, Edge, Safari |

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/santa-cruz-segura.git
cd santa-cruz-segura
```

### 2. Crear entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=santa_cruz_segura
DB_USER=root
DB_PASSWORD=tu_contraseña

SECRET_KEY=genera_una_clave_muy_segura_al_menos_64_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

APP_ENV=development
UPLOAD_DIR=uploads/
MAX_UPLOAD_MB=10
```

### 5. Crear la base de datos

Ejecuta el script SQL completo en MySQL Workbench o línea de comandos:

```sql
CREATE DATABASE IF NOT EXISTS santa_cruz_segura
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE santa_cruz_segura;
-- (Resto del script SQL proporcionado en la documentación)
```

### 6. Entrenar el modelo de Machine Learning

```bash
python backend/ml/train.py
```

Este comando genera el archivo `backend/ml/model.pkl` con el Random Forest entrenado.

---

## 🚀 Ejecución Local

### Iniciar el servidor FastAPI

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

| Parámetro | Descripción |
|-----------|-------------|
| `--reload` | Reinicio automático en desarrollo (no usar en producción) |
| `--host` | Dirección de escucha (127.0.0.1 solo local, 0.0.0.0 para red local) |
| `--port` | Puerto de la aplicación |

### Acceder a la aplicación

| Recurso | URL |
|---------|-----|
| **Aplicación web** | http://localhost:8000 |
| **Documentación API (Swagger)** | http://localhost:8000/docs |
| **Documentación API (Redoc)** | http://localhost:8000/redoc |
| **WebSocket Mapa** | ws://localhost:8000/ws/mapa |

---

## ☁️ Despliegue en Railway

Railway es la plataforma recomendada para producción por su simplicidad y soporte nativo para Python.

### Pasos para desplegar:

1. **Crear cuenta en Railway**: https://railway.app
2. **Conectar repositorio GitHub**: Railway → New Project → Deploy from GitHub repo
3. **Configurar variables de entorno**: Railway Dashboard → Variables → Añadir cada variable del `.env`
4. **Añadir base de datos MySQL**: Railway → New → Database → MySQL (Railway aprovisiona automáticamente)
5. **Railway ejecuta automáticamente**: Detecta `requirements.txt` y ejecuta `railway.json`

### Archivo `railway.json` incluido:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

---

## 🗄️ Base de Datos

### Modelo Entidad-Relación (simplificado)

```
usuario (id_usuario, nombre, apellido, email, password_hash, id_junta, id_rol)
    │
    ├──< reporte (id_reporte, latitud, longitud, estado, anonimo, id_usuario, id_zona, id_tipo)
    │       │
    │       └──< evidencia (id_evidencia, tipo_archivo, ruta_archivo, id_reporte)
    │
    ├──< alerta (id_alerta, titulo, tipo, estado, id_creador, id_zona, id_junta)
    │       │
    │       └──< notificacion (id_notificacion, mensaje, id_alerta)
    │               │
    │               └──< usuario_notificacion (id_usuario, id_notificacion, leida)
    │
    └──> rol (id_rol, nombre)

junta_vecinal (id_junta, nombre, distrito)
    │
    ├──< usuario
    └──< zona_caliente (id_zona, nombre, latitud_centro, longitud_centro, radio_metros, nivel_riesgo, id_junta)
            │
            ├──< reporte
            ├──< alerta
            └──< prediccion_ia (id_prediccion, nivel_predicho, probabilidad, periodo_inicio, periodo_fin, id_zona)
```

### Trigger automático

```sql
CREATE TRIGGER trg_actualizar_zona_riesgo
AFTER INSERT ON reporte
FOR EACH ROW
BEGIN
  UPDATE zona_caliente
  SET total_reportes_30d = (
    SELECT COUNT(*) FROM reporte
    WHERE id_zona = NEW.id_zona AND fecha_reporte >= DATE_SUB(NOW(), INTERVAL 30 DAY)
  ),
  nivel_riesgo = CASE
    WHEN total_reportes_30d >= 20 THEN 'critico'
    WHEN total_reportes_30d >= 10 THEN 'alto'
    WHEN total_reportes_30d >= 5  THEN 'medio'
    ELSE 'bajo'
  END
  WHERE id_zona = NEW.id_zona;
END;
```

---

## 📡 Endpoints de la API

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Rol requerido |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Iniciar sesión, devuelve JWT | Público |
| POST | `/auth/register` | Registrar nuevo usuario (rol vecino por defecto) | Público |
| GET | `/auth/juntas` | Listar juntas vecinales | Público |
| GET | `/auth/tipos` | Listar tipos de incidente | Público |

### Usuarios (`/usuarios`)

| Método | Endpoint | Descripción | Rol requerido |
|--------|----------|-------------|---------------|
| GET | `/usuarios/me` | Obtener datos del usuario autenticado | Autenticado |
| PUT | `/usuarios/me/password` | Cambiar contraseña | Autenticado |
| GET | `/usuarios` | Listar todos los usuarios | Admin |
| PUT | `/usuarios/{id}/estado` | Activar/suspender usuario | Admin |
| PUT | `/usuarios/{id}/rol` | Cambiar rol (1-4) | Admin |

### Reportes (`/reportes`)

| Método | Endpoint | Descripción | Rol requerido |
|--------|----------|-------------|---------------|
| POST | `/reportes` | Crear nuevo reporte | Autenticado |
| GET | `/reportes/mis` | Reportes del usuario actual | Autenticado |
| GET | `/reportes` | Listar reportes (con filtros opcionales) | Autenticado |
| GET | `/reportes/gestion` | Listar todos con info del reportante | Directivo/Autoridad/Admin |
| PUT | `/reportes/{id}/estado` | Cambiar estado | Directivo/Admin |
| POST | `/reportes/{id}/evidencia` | Subir archivo evidencia | Autenticado |

### Zonas (`/zonas`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/zonas` | Listar zonas con distrito y nivel de riesgo |
| GET | `/zonas/{id}/heatmap` | Puntos de calor con intensidad |

### Alertas (`/alertas`)

| Método | Endpoint | Descripción | Rol requerido |
|--------|----------|-------------|---------------|
| GET | `/alertas` | Listar alertas activas | Autenticado |
| POST | `/alertas` | Crear nueva alerta | Directivo/Admin |
| PUT | `/alertas/{id}/cerrar` | Marcar alerta como resuelta | Directivo/Admin |

### Dashboard (`/dashboard`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/dashboard/resumen` | Resumen por barrio (vista v_resumen_barrio) |
| GET | `/dashboard/tendencia` | Reportes diarios últimos 30 días |
| GET | `/dashboard/tipos` | Distribución por tipo de incidente |

### Inteligencia Artificial (`/ia`)

| Método | Endpoint | Descripción | Rol requerido |
|--------|----------|-------------|---------------|
| POST | `/ia/predecir/{id_zona}` | Generar nueva predicción | Directivo/Autoridad/Admin |
| GET | `/ia/predicciones` | Última predicción por zona | Autenticado |

---

## 🤖 Modelo de Machine Learning

### Algoritmo: Random Forest Classifier

| Parámetro | Valor |
|-----------|-------|
| **n_estimators** | 100 árboles |
| **random_state** | 42 (semilla fija) |
| **Característica de entrada** | total_reportes_30d (entero) |
| **Clases de salida** | bajo (0), medio (1), alto (2), crítico (3) |

### Datos de entrenamiento (sintéticos)

| Rango de reportes | Cantidad muestras | Etiqueta |
|-------------------|-------------------|----------|
| 0 - 4 | 200 | bajo |
| 5 - 9 | 150 | medio |
| 10 - 19 | 100 | alto |
| 20 - 50 | 50 | crítico |

### Lógica heurística de respaldo

Si el archivo `model.pkl` no existe, el sistema usa esta lógica simple:

| total_reportes_30d | Nivel predicho | Probabilidad |
|--------------------|----------------|--------------|
| >= 20 | crítico | 0.90 |
| >= 10 | alto | 0.75 |
| >= 5 | medio | 0.60 |
| < 5 | bajo | 0.85 |

---

## 🔌 WebSockets en Tiempo Real

### Conexión

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/mapa');
```

### Mensaje de nuevo reporte (broadcast)

```json
{
  "tipo": "nuevo_reporte",
  "id_reporte": 123,
  "latitud": -17.7834,
  "longitud": -63.1821,
  "tipo_incidente": "Robo a transeúnte",
  "nivel_zona": "alto",
  "id_zona": 5
}
```

### Flujo

1. Usuario A crea un reporte en `/reportes` (POST)
2. Backend guarda en MySQL
3. Backend llama a `manager.broadcast(evento)`
4. Todos los usuarios conectados a `/ws/mapa` reciben el mensaje
5. Frontend ejecuta `agregarMarcadorNuevo()` con animación

---

## 👥 Roles y Permisos

| Rol | ID | Descripción | Permisos principales |
|-----|-----|-------------|----------------------|
| **Vecino** | 1 | Ciudadano del barrio | Reportar incidentes, ver mapa, ver alertas, ver sus reportes |
| **Directivo** | 2 | Miembro de junta vecinal | Todo lo de vecino + gestionar reportes, crear/cerrar alertas, ejecutar predicciones IA |
| **Autoridad** | 3 | Policía o municipal | Todo lo de vecino + gestionar reportes (solo lectura), ejecutar predicciones IA |
| **Admin** | 4 | Administrador del sistema | Todos los permisos + gestionar usuarios (cambiar rol, activar/suspender) |

---

## 👨‍💻 Manual de Usuario

### Registro e inicio de sesión

1. Accede a `http://localhost:8000` o la URL desplegada
2. En la pestaña "Registrarse", completa tus datos (nombre, apellido, email, contraseña, junta vecinal)
3. Una vez registrado, inicia sesión con tu email y contraseña
4. El sistema te redirige al Dashboard principal

### Reportar un incidente

1. Ve a la página **Reportar** desde el menú lateral
2. Haz clic en cualquier punto del mapa donde ocurrió el incidente
3. Se abrirá un modal. Selecciona el tipo de incidente, verifica la zona automática
4. Completa descripción opcional, fecha/hora, y opcionalmente adjunta evidencia
5. Marca "Reportar anónimamente" si deseas ocultar tu identidad
6. Haz clic en "Enviar reporte". El mapa se actualizará para todos los usuarios conectados

### Ver mis reportes

1. Ve a **Mis reportes** en el menú lateral
2. Verás todas tus denuncias en formato de tarjetas, con estado y nivel de riesgo
3. Puedes filtrar por estado (pendiente, verificado, resuelto, descartado)

### Gestionar reportes (Directivo/Autoridad/Admin)

1. Ve a **Gestionar reportes** en el menú lateral
2. Usa los filtros de estado, tipo y zona para acotar la lista
3. Haz clic en "Ver detalle" para ver toda la información del reporte
4. Usa los botones de acción para cambiar el estado (verificar, resolver, descartar)

### Crear alerta (Directivo/Admin)

1. Ve a **Alertas** y haz clic en "Nueva alerta"
2. Completa título, tipo (preventiva/reactiva/informativa), zona y junta
3. Opcionalmente agrega descripción y fecha de cierre
4. Publica la alerta. Aparecerá en el banner del dashboard y en la página de alertas

### Panel de administración (Admin)

1. Ve a **Usuarios** en el menú lateral
2. Verás la lista completa de usuarios registrados
3. Para cambiar rol, haz clic en "Rol" y selecciona nuevo rol (Vecino/Directivo/Autoridad/Admin)
4. Para activar/suspender, haz clic en "Activar" o "Suspender" según corresponda

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. **Fork** el repositorio
2. Crea una **rama de características** (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Guías de estilo

- **Python**: Sigue PEP 8. Usa 4 espacios para indentación.
- **JavaScript**: Usa camelCase para variables y funciones.
- **CSS/HTML**: Usa clases en kebab-case.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.

---

## 📞 Contacto

| Recurso | Enlace |
|---------|--------|
| **Documentación completa** | [Google Drive](https://drive.google.com/drive/folders/1HXZqqYPVU5HvbYCr5LiGRrGLIiw-v56L?usp=sharing) |
| **Repositorio** | [GitHub](https://github.com/Angellec21/santa-cruz-segura) |
| **Reporte de bugs** | [Issues](https://github.com/Angellec21/santa-cruz-segura/issues) |
| **Correo** | soporte@santacruzsegura.bo |

---

<div align="center">
  <sub>Desarrollado con ❤️ para Santa Cruz de la Sierra, Bolivia</sub>
</div>
```