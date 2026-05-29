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


def guardar_evidencia(id_reporte: int, archivo: UploadFile, db: Session) -> Evidencia:
    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    ext = archivo.filename.rsplit(".", 1)[-1].lower()
    tipo_map = {
        "jpg": TipoArchivo.imagen, "jpeg": TipoArchivo.imagen, "png": TipoArchivo.imagen,
        "mp4": TipoArchivo.video, "avi": TipoArchivo.video,
        "mp3": TipoArchivo.audio, "wav": TipoArchivo.audio,
    }
    tipo = tipo_map.get(ext, TipoArchivo.imagen)

    nombre_guardado = f"{uuid.uuid4()}.{ext}"
    ruta = os.path.join(settings.UPLOAD_DIR, nombre_guardado)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    with open(ruta, "wb") as f:
        f.write(archivo.file.read())

    evidencia = Evidencia(
        id_reporte=id_reporte,
        tipo_archivo=tipo,
        ruta_archivo=ruta,
        nombre_original=archivo.filename,
    )
    db.add(evidencia)
    db.commit()
    db.refresh(evidencia)
    return evidencia
