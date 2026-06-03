from __future__ import annotations
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.usuario import Usuario
from backend.schemas.auth import RegisterRequest
from backend.utils.security import (
    hash_password, verify_password, create_access_token,
    generate_token, generate_session_id,
)

ROL_VECINO_ID = 1


def login(email: str, password: str, db: Session) -> str:
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    if not user.activo:
        raise HTTPException(status_code=403, detail="Cuenta suspendida")
    if not user.email_verificado:
        raise HTTPException(
            status_code=403,
            detail="Debes verificar tu correo antes de ingresar. Revisa tu bandeja de entrada.",
        )

    # Sesión única: nuevo session_id invalida dispositivos anteriores
    session_id = generate_session_id()
    user.session_id = session_id
    db.commit()

    return create_access_token({"sub": str(user.id_usuario), "sid": session_id})


def register(data: RegisterRequest, db: Session) -> Usuario:
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="El email ya está registrado")

    token = generate_token()
    user = Usuario(
        id_junta=data.id_junta,
        id_rol=ROL_VECINO_ID,
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        telefono=data.telefono,
        password_hash=hash_password(data.password),
        email_verificado=False,
        token_verificacion=token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    try:
        from backend.services.email_service import enviar_verificacion
        enviar_verificacion(user.email, user.nombre, token)
    except Exception:
        pass  # No bloquea el registro si el email falla

    return user


def verificar_email(token: str, db: Session) -> bool:
    user = db.query(Usuario).filter(Usuario.token_verificacion == token).first()
    if not user:
        return False
    user.email_verificado = True
    user.token_verificacion = None
    db.commit()
    return True
