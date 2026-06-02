from __future__ import annotations
import os
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from backend.models.reporte import Reporte
from backend.models.evidencia import Evidencia, TipoArchivo
from backend.models.zona_caliente import ZonaCaliente
from backend.schemas.reporte import ReporteCreate, ReporteEstadoUpdate
from backend.config import settings


def crear_reporte(data: ReporteCreate, id_usuario: int, db: Session) -> Reporte:
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
    return reporte


def listar_reportes(
    db: Session,
    id_zona: int | None = None,
    id_tipo: int | None = None,
    estado: str | None = None,
    id_usuario: int | None = None,
) -> list[Reporte]:
    q = db.query(Reporte)
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

    nombre_guardado = f"{uuid.uuid4()}.{ext}"
    upload_dir = settings.UPLOAD_DIR.rstrip("/")
    os.makedirs(upload_dir, exist_ok=True)

    ruta_local = os.path.join(upload_dir, nombre_guardado)
    with open(ruta_local, "wb") as f:
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
