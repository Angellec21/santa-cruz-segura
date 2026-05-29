from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioResponse, UsuarioEstadoUpdate
from backend.utils.deps import get_db, get_current_user, require_role, ROL_ADMIN

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.get("", response_model=list[UsuarioResponse])
def listar(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role([ROL_ADMIN])),
):
    return db.query(Usuario).all()


@router.put("/{id_usuario}/estado", response_model=UsuarioResponse)
def cambiar_estado(
    id_usuario: int,
    data: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role([ROL_ADMIN])),
):
    user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.activo = data.activo
    db.commit()
    db.refresh(user)
    return user
