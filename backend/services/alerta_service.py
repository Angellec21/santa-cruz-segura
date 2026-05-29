from __future__ import annotations
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.alerta import Alerta, EstadoAlerta
from backend.schemas.alerta import AlertaCreate


def listar_alertas(db: Session) -> list[Alerta]:
    return (
        db.query(Alerta)
        .filter(Alerta.estado == EstadoAlerta.activa)
        .order_by(Alerta.fecha_inicio.desc())
        .all()
    )


def crear_alerta(data: AlertaCreate, id_creador: int, db: Session) -> Alerta:
    alerta = Alerta(
        id_zona=data.id_zona,
        id_junta=data.id_junta,
        id_creador=id_creador,
        titulo=data.titulo,
        descripcion=data.descripcion,
        tipo=data.tipo,
        fecha_fin=data.fecha_fin,
    )
    db.add(alerta)
    db.commit()
    db.refresh(alerta)
    return alerta


def cerrar_alerta(id_alerta: int, db: Session) -> Alerta:
    alerta = db.query(Alerta).filter(Alerta.id_alerta == id_alerta).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    alerta.estado = EstadoAlerta.resuelta
    db.commit()
    db.refresh(alerta)
    return alerta
