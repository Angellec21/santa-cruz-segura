from __future__ import annotations
import io
import math
import os
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, UploadFile
from backend.models.reporte import Reporte, EstadoReporte
from backend.models.evidencia import Evidencia, TipoArchivo
from backend.models.zona_caliente import ZonaCaliente
from backend.schemas.reporte import ReporteCreate, ReporteEstadoUpdate
from backend.config import settings
from backend.utils import cache
from backend.websocket.manager import manager

_STOP_WORDS = {
    'el','la','los','las','un','una','de','del','en','y','a','que','se',
    'con','por','al','es','fue','hay','no','su','sus','me','te','le','lo',
    'mi','tu','si','ya','o','e','ni','más','muy','era','han','hay','este',
    'esta','esto','eso','esa','aqui','ahi','alla','como','cuando','donde',
    'quien','cual','para','pero','más','también','solo','todo','todos',
}


def _distancia_metros(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _palabras_significativas(texto: str) -> set[str]:
    if not texto:
        return set()
    return {w for w in texto.lower().split() if len(w) > 2 and w not in _STOP_WORDS}


def _buscar_duplicado(data: ReporteCreate, db: Session) -> Reporte | None:
    """Detecta si existe un reporte similar: mismo lugar (<100m), últimos 30 min,
    descripción con ≥2 palabras en común (excluyendo stop words)."""
    hace_30min = datetime.now(timezone.utc) - timedelta(minutes=30)

    candidatos = db.query(Reporte).filter(
        Reporte.id_zona == data.id_zona,
        Reporte.id_tipo == data.id_tipo,
        Reporte.fecha_reporte >= hace_30min,
        Reporte.estado != EstadoReporte.descartado,
    ).all()

    palabras_nuevo = _palabras_significativas(data.descripcion or "")

    for r in candidatos:
        dist = _distancia_metros(
            float(data.latitud), float(data.longitud),
            float(r.latitud), float(r.longitud),
        )
        if dist > 100:
            continue

        # Sin descripción: misma zona + mismo tipo + <50m = duplicado
        if not data.descripcion or not r.descripcion:
            if dist <= 50:
                return r
            continue

        coincidencias = palabras_nuevo & _palabras_significativas(r.descripcion)
        if len(coincidencias) >= 2:
            return r

    return None


def crear_reporte(data: ReporteCreate, id_usuario: int, db: Session) -> Reporte:
    # Rate limit: 1 reporte por usuario cada 5 minutos
    reciente = db.query(Reporte).filter(
        Reporte.id_usuario == id_usuario,
        Reporte.fecha_reporte >= datetime.now(timezone.utc) - timedelta(minutes=5),
    ).first()
    if reciente:
        raise HTTPException(
            status_code=429,
            detail="Solo puedes enviar un reporte cada 5 minutos. Intenta más tarde.",
        )

    # Deduplicación: detectar incidente ya reportado
    duplicado = _buscar_duplicado(data, db)
    if duplicado:
        raise HTTPException(
            status_code=409,
            detail=(
                f"DUPLICADO:{duplicado.id_reporte}|"
                f"Este incidente ya fue reportado (#{duplicado.id_reporte}). "
                f"Tu confirmación suma al reporte existente. ¡Gracias!"
            ),
        )

    zona = db.query(ZonaCaliente).filter(ZonaCaliente.id_zona == data.id_zona).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    reporte = Reporte(
        id_usuario=id_usuario,
        id_zona=data.id_zona,
        id_tipo=data.id_tipo,
        descripcion=data.descripcion,
        latitud=data.latitud,
        longitud=data.longitud,
        anonimo=data.anonimo,
        fecha_incidente=data.fecha_incidente,
    )
    db.add(reporte)
    db.commit()
    db.refresh(reporte)
    cache.invalidate("dashboard:resumen", "dashboard:tendencia", "dashboard:tipos", "zonas:list")
    cache.invalidate_prefix("zonas:heatmap:")

    db.refresh(zona)  # el trigger ya recalculó nivel_riesgo dentro de la misma transacción
    manager.broadcast({
        "tipo": "nuevo_reporte",
        "id_reporte": reporte.id_reporte,
        "latitud": float(reporte.latitud),
        "longitud": float(reporte.longitud),
        "tipo_incidente": reporte.tipo_incidente.nombre if reporte.tipo_incidente else None,
        "nivel_zona": zona.nivel_riesgo.value,
        "id_zona": zona.id_zona,
    })
    return reporte


def listar_incidentes(lat: float, lng: float, db: Session) -> list[tuple[Reporte, float]]:
    """Incidentes pendientes (sin autoridad asignada) ordenados por distancia al usuario."""
    reportes = db.query(Reporte).options(selectinload(Reporte.evidencias)).filter(
        Reporte.estado == EstadoReporte.pendiente,
        Reporte.id_autoridad == None,
    ).all()
    con_distancia = [
        (r, _distancia_metros(lat, lng, float(r.latitud), float(r.longitud)))
        for r in reportes
    ]
    con_distancia.sort(key=lambda x: x[1])
    return con_distancia


def asignar_caso(id_reporte: int, id_autoridad: int, db: Session) -> Reporte:
    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    if reporte.id_autoridad:
        raise HTTPException(status_code=409, detail="Este incidente ya fue asignado a otra autoridad")
    reporte.id_autoridad = id_autoridad
    reporte.estado = EstadoReporte.verificado
    db.commit()
    db.refresh(reporte)
    cache.invalidate_prefix("zonas:heatmap:")
    return reporte


def listar_mis_casos(id_autoridad: int, db: Session) -> dict:
    activos = db.query(Reporte).options(selectinload(Reporte.evidencias)).filter(
        Reporte.id_autoridad == id_autoridad,
        Reporte.estado == EstadoReporte.verificado,
    ).order_by(Reporte.fecha_reporte.desc()).all()

    historial = db.query(Reporte).options(selectinload(Reporte.evidencias)).filter(
        Reporte.id_autoridad == id_autoridad,
        Reporte.estado == EstadoReporte.resuelto,
    ).order_by(Reporte.fecha_reporte.desc()).all()

    return {"activos": activos, "historial": historial}


def resolver_caso(id_reporte: int, id_autoridad: int, db: Session) -> Reporte:
    reporte = db.query(Reporte).filter(
        Reporte.id_reporte == id_reporte,
        Reporte.id_autoridad == id_autoridad,
    ).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Caso no encontrado o no asignado a ti")
    reporte.estado = EstadoReporte.resuelto
    db.commit()
    db.refresh(reporte)
    # Quitar del mapa en tiempo real invalidando todos los cachés
    cache.invalidate("dashboard:resumen", "dashboard:tendencia", "zonas:list")
    cache.invalidate_prefix("zonas:heatmap:")
    return reporte


def listar_reportes(
    db: Session,
    id_zona: int | None = None,
    id_tipo: int | None = None,
    estado: str | None = None,
    id_usuario: int | None = None,
    with_evidencias: bool = False,
) -> list[Reporte]:
    q = db.query(Reporte)
    if with_evidencias:
        q = q.options(selectinload(Reporte.evidencias))
    if id_zona:
        q = q.filter(Reporte.id_zona == id_zona)
    if id_tipo:
        q = q.filter(Reporte.id_tipo == id_tipo)
    if estado:
        q = q.filter(Reporte.estado == estado)
    if id_usuario:
        q = q.filter(Reporte.id_usuario == id_usuario)
    return q.order_by(Reporte.fecha_reporte.desc()).all()


def actualizar_estado(id_reporte: int, data: ReporteEstadoUpdate, db: Session) -> Reporte:
    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    reporte.estado = data.estado
    db.commit()
    db.refresh(reporte)
    return reporte


async def guardar_evidencia(id_reporte: int, archivo: UploadFile, db: Session) -> Evidencia:
    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    contenido = await archivo.read()
    limite = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(contenido) > limite:
        raise HTTPException(status_code=413, detail=f"El archivo excede el límite de {settings.MAX_UPLOAD_MB} MB")
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío")

    nombre = archivo.filename or "archivo"
    ext = nombre.rsplit(".", 1)[-1].lower() if "." in nombre else "jpg"
    tipo_map = {
        "jpg": TipoArchivo.imagen, "jpeg": TipoArchivo.imagen,
        "png": TipoArchivo.imagen, "gif": TipoArchivo.imagen, "webp": TipoArchivo.imagen,
        "mp4": TipoArchivo.video, "avi": TipoArchivo.video,
        "mov": TipoArchivo.video, "webm": TipoArchivo.video,
        "mp3": TipoArchivo.audio, "wav": TipoArchivo.audio, "ogg": TipoArchivo.audio,
    }
    tipo = tipo_map.get(ext, TipoArchivo.imagen)

    if settings.CLOUDINARY_URL:
        p = urlparse(settings.CLOUDINARY_URL)
        cloudinary.config(cloud_name=p.hostname, api_key=p.username, api_secret=p.password)
        resource = "video" if tipo == TipoArchivo.video else "auto"
        result = cloudinary.uploader.upload(
            io.BytesIO(contenido),
            resource_type=resource,
            folder="santa-cruz-segura",
            public_id=str(uuid.uuid4()),
        )
        url_publica = result["secure_url"]
    else:
        nombre_guardado = f"{uuid.uuid4()}.{ext}"
        upload_dir = settings.UPLOAD_DIR.rstrip("/")
        os.makedirs(upload_dir, exist_ok=True)
        with open(os.path.join(upload_dir, nombre_guardado), "wb") as f:
            f.write(contenido)
        url_publica = f"/{upload_dir}/{nombre_guardado}"

    evidencia = Evidencia(
        id_reporte=id_reporte,
        tipo_archivo=tipo,
        ruta_archivo=url_publica,
        nombre_original=nombre,
    )
    db.add(evidencia)
    db.commit()
    db.refresh(evidencia)
    return evidencia
