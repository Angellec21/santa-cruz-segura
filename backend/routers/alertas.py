from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.schemas.alerta import AlertaCreate, AlertaResponse
from backend.services import alerta_service
from backend.utils.deps import get_db, get_current_user, require_role, ROL_DIRECTIVO, ROL_ADMIN

router = APIRouter(prefix="/alertas", tags=["alertas"])


@router.get("", response_model=list[AlertaResponse])
def listar(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return alerta_service.listar_alertas(db)


@router.post("", response_model=AlertaResponse, status_code=201)
def crear(
    data: AlertaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role([ROL_DIRECTIVO, ROL_ADMIN])),
):
    return alerta_service.crear_alerta(data, current_user.id_usuario, db)


@router.put("/{id_alerta}/cerrar", response_model=AlertaResponse)
def cerrar(
    id_alerta: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role([ROL_DIRECTIVO, ROL_ADMIN])),
):
    return alerta_service.cerrar_alerta(id_alerta, db)
