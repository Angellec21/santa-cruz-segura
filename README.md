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