from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioResponse, UsuarioEstadoUpdate, UsuarioRolUpdate, PasswordChange
from backend.utils.security import hash_password, verify_password
from backend.utils.deps import get_db, get_current_user, require_role, ROL_ADMIN

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.put("/me/password")
def cambiar_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if not verify_password(data.password_actual, current_user.password_hash):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
    if len(data.password_nueva) < 6:
        raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 6 caracteres")
    current_user.password_hash = hash_password(data.password_nueva)
    db.commit()
    return {"mensaje": "Contraseña actualizada correctamente"}


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


@router.put("/{id_usuario}/rol", response_model=UsuarioResponse)
def cambiar_rol(
    id_usuario: int,
    data: UsuarioRolUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role([ROL_ADMIN])),
):
    user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if data.id_rol not in (1, 2, 3, 4):
        raise HTTPException(status_code=400, detail="Rol inválido")
    user.id_rol = data.id_rol
    db.commit()
    db.refresh(user)
    return user
