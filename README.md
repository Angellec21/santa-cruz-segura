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
| **Autenticación** | Registro e inicio de sesión con JWT |
| **Roles de usuario** | Vecino, Directivo, Autoridad, Administrador con permisos diferenciados |
| **Mapa interactivo** | Visualización de zonas calientes, círculos de riesgo, mapa de calor |
| **Reportes** | Creación de incidentes con geolocalización, evidencias y opción anónima |
| **Alertas** | Emisión y gestión de alertas preventivas, reactivas e informativas |
| **IA Predictiva** | Predicción de nivel de riesgo para los próximos 7 días |
| **Tiempo real** | WebSockets que actualizan el mapa instantáneamente |
| **Dashboard** | Métricas, gráficas de tendencia, resumen por barrio |
| **Panel admin** | Gestión de usuarios, cambio de roles, activación/suspensión |

---

## 🛠️ Tecnologías Utilizadas

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| FastAPI | 0.111.0 | Framework web principal |
| Uvicorn | 0.29.0 | Servidor ASGI |
| SQLAlchemy | 2.0.30 | ORM para base de datos |
| PyMySQL | 1.1.0 | Conector MySQL |
| Python-JOSE | 3.3.0 | Tokens JWT |
| bcrypt | 4.2.1 | Hashing de contraseñas |
| Pydantic | 2.7.1 | Validación de datos |

### Machine Learning

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Scikit-learn | 1.6.1 | Random Forest Classifier |
| NumPy | 2.2.6 | Datos sintéticos |
| Pandas | 2.2.3 | Manipulación de datos |

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| HTML5 + CSS3 | - | Estructura y estilos |
| Bootstrap 5 | 5.3.3 | Componentes responsivos |
| Leaflet | 1.9.4 | Mapas interactivos |
| Leaflet.heat | 0.2.0 | Mapa de calor |
| Chart.js | 4.4.2 | Gráficas |
| WebSocket API | - | Tiempo real |

### Base de Datos

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| MySQL | 8.0 | Motor de base de datos |
| Triggers | - | Actualización automática de riesgos |
| Views | - | Resúmenes precalculados |

### Despliegue

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Railway | - | Plataforma cloud |
| Git | - | Control de versiones |

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph TD
    subgraph Cliente
        A[Frontend<br/>HTML + CSS + JavaScript]
        A1[Bootstrap 5]
        A2[Leaflet Mapas]
        A3[WebSocket Client]
    end

    subgraph Servidor
        B[FastAPI Backend]
        B1[Routers]
        B2[Services]
        B3[WebSocket Manager]
    end

    subgraph ML
        C[Random Forest<br/>Modelo Predictivo]
    end

    subgraph DB
        D[(MySQL)]
        D1[Usuarios]
        D2[Reportes]
        D3[Zonas]
        D4[Alertas]
    end

    A -->|HTTP / WebSocket| B
    B --> C
    B --> D
    B1 --> B2
    B2 --> D
    B3 -->|Broadcast| A
    C -->|Predicción| B

    Flujo principal de datos:

El usuario interactúa con el frontend (Bootstrap + Leaflet)

Las peticiones HTTP viajan al backend FastAPI

Los routers dirigen a los servicios correspondientes

Los servicios consultan o actualizan MySQL

El WebSocket Manager envía eventos en tiempo real a todos los clientes

El modelo Random Forest predice niveles de riesgo bajo demanda


📁 Estructura del Proyecto

santa-cruz-segura/
│
├── backend/
│   ├── ml/
│   │   ├── predictor.py
│   │   └── train.py
│   ├── models/
│   │   ├── usuario.py
│   │   ├── reporte.py
│   │   ├── zona_caliente.py
│   │   ├── alerta.py
│   │   └── ...
│   ├── routers/
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── reportes.py
│   │   ├── zonas.py
│   │   ├── alertas.py
│   │   ├── dashboard.py
│   │   └── ia.py
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   │   ├── deps.py
│   │   └── security.py
│   ├── websocket/
│   │   └── manager.py
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── frontend/
│   ├── js/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── mapa.js
│   │   ├── dashboard.js
│   │   ├── alertas.js
│   │   └── reportar.js
│   ├── css/
│   ├── assets/
│   ├── index.html
│   ├── dashboard.html
│   ├── reportar.html
│   ├── mis-reportes.html
│   ├── gestionar-reportes.html
│   ├── alertas.html
│   └── admin.html
│
├── uploads/
├── .env.example
├── .gitignore
├── requirements.txt
├── railway.json
└── README.md


📋 Requisitos Previos
Requisito	Versión
Python	3.9+
MySQL	8.0+
pip	última versión
Git	2.x+ (opcional)
Navegador	Chrome, Firefox, Edge, Safari

⚙️ Instalación y Configuración
1. Clonar el repositorio
git clone https://github.com/tu-usuario/santa-cruz-segura.git
cd santa-cruz-segura

2. Crear entorno virtual
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

4. Configurar variables de entorno
Crea un archivo .env en la raíz:
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

5. Crear la base de datos
Ejecuta el script SQL completo en MySQL Workbench.

6. Entrenar el modelo de Machine Learning
python backend/ml/train.py
Esto genera backend/ml/model.pkl.

🚀 Ejecución Local
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

Recurso	URL
Aplicación web	http://localhost:8000
Documentación API (Swagger)	http://localhost:8000/docs
Documentación API (Redoc)	http://localhost:8000/redoc
WebSocket Mapa	ws://localhost:8000/ws/mapa

☁️ Despliegue en Railway
Crear cuenta en https://railway.app

Conectar repositorio GitHub

Configurar variables de entorno

Añadir base de datos MySQL

Railway ejecuta automáticamente con railway.json

Archivo railway.json incluido:
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

🗄️ Base de Datos
Modelo simplificado
usuario: id_usuario, nombre, email, password_hash, id_junta, id_rol

junta_vecinal: id_junta, nombre, distrito

zona_caliente: id_zona, nombre, latitud, longitud, radio, nivel_riesgo

reporte: id_reporte, latitud, longitud, estado, anonimo, id_zona, id_tipo

evidencia: id_evidencia, tipo_archivo, ruta, id_reporte

alerta: id_alerta, titulo, tipo, estado, id_zona

prediccion_ia: id_prediccion, nivel_predicho, probabilidad, id_zona

Trigger automático
Cuando se inserta un reporte, se actualiza el nivel de riesgo de la zona según la cantidad de reportes en los últimos 30 días.

📡 Endpoints de la API
Método	Endpoint	Descripción	Rol
POST	/auth/login	Iniciar sesión	Público
POST	/auth/register	Registrar usuario	Público
GET	/usuarios/me	Mi perfil	Autenticado
POST	/reportes	Crear reporte	Autenticado
GET	/reportes/mis	Mis reportes	Autenticado
GET	/reportes/gestion	Todos los reportes	Directivo/Autoridad/Admin
PUT	/reportes/{id}/estado	Cambiar estado	Directivo/Admin
GET	/zonas	Listar zonas	Autenticado
GET	/alertas	Alertas activas	Autenticado
POST	/alertas	Crear alerta	Directivo/Admin
POST	/ia/predecir/{id}	Predecir riesgo	Directivo/Autoridad/Admin
GET	/dashboard/resumen	Estadísticas	Autenticado
🤖 Modelo de Machine Learning
Algoritmo: Random Forest Classifier (100 árboles)

Característica de entrada: total_reportes_30d

Clases de salida: bajo (0), medio (1), alto (2), crítico (3)

Datos de entrenamiento (sintéticos):

Reportes 30d	Muestras	Etiqueta
0 - 4	200	bajo
5 - 9	150	medio
10 - 19	100	alto
20 - 50	50	crítico
Precisión en datos sintéticos: >95%

🔌 WebSockets en Tiempo Real
Conexión:
const ws = new WebSocket('ws://localhost:8000/ws/mapa');

Mensaje de nuevo reporte:
{
  "tipo": "nuevo_reporte",
  "id_reporte": 123,
  "latitud": -17.7834,
  "longitud": -63.1821,
  "tipo_incidente": "Robo a transeúnte",
  "nivel_zona": "alto",
  "id_zona": 5
}

Flujo:

Usuario A crea un reporte

Backend guarda en MySQL

Backend emite broadcast a todos los clientes conectados

Todos ven el nuevo marcador con animación

👥 Roles y Permisos
Rol	ID	Permisos principales
Vecino	1	Reportar, ver mapa y alertas, ver sus reportes
Directivo	2	Todo lo de vecino + gestionar reportes, crear alertas, predecir IA
Autoridad	3	Todo lo de vecino + gestionar reportes (lectura), predecir IA
Admin	4	Todos los permisos + gestionar usuarios
👨‍💻 Manual de Usuario
Registro e inicio de sesión
Accede a http://localhost:8000

Pestaña "Registrarse" → completa tus datos

Inicia sesión con email y contraseña

Reportar un incidente
Ve a Reportar

Haz clic en el mapa donde ocurrió el incidente

Completa el modal (tipo, zona, descripción, fecha)

Opcional: adjunta evidencia o marca anónimo

Enviar reporte → se actualiza para todos

Ver mis reportes
Ve a Mis reportes

Verás todas tus denuncias en tarjetas

Filtra por estado (pendiente, verificado, resuelto, descartado)

Gestionar reportes (Directivo/Autoridad/Admin)
Ve a Gestionar reportes

Usa filtros para acotar la lista

Cambia estados: verificar, resolver, descartar

Crear alerta (Directivo/Admin)
Ve a Alertas → "Nueva alerta"

Completa título, tipo, zona, junta

Publicar → aparece en el dashboard

Panel de administración (Admin)
Ve a Usuarios

Lista completa de usuarios

Cambiar rol o activar/suspender cuentas

🤝 Contribuciones
Fork el repositorio

Rama de características (git checkout -b feature/nueva-funcionalidad)

Commit (git commit -m 'Agrega nueva funcionalidad')

Push (git push origin feature/nueva-funcionalidad)

Pull Request

Guías de estilo:

Python: PEP 8, 4 espacios

JavaScript: camelCase

CSS/HTML: kebab-case

📄 Licencia
UPDS
📞 Contacto
| Recurso | Enlace | |---------|--------| | **Documentación completa** | [Google Drive](https://drive.google.com/drive/folders/1HXZqqYPVU5HvbYCr5LiGRrGLIiw-v56L?usp=sharing) | | **Repositorio** | [GitHub](https://github.com/Angellec21/santa-cruz-segura) | | **Reporte de bugs** | [Issues](https://github.com/Angellec21/santa-cruz-segura/issues) | | **Correo** | soporte@santacruzsegura.bo |