from __future__ import annotations
import random
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.usuario import Usuario
from backend.schemas.auth import RegisterRequest
from backend.utils.security import (
    hash_password, verify_password, create_access_token,
    generate_session_id,
)

ROL_VECINO_ID = 1


def _generar_codigo() -> str:
    return str(random.randint(100000, 999999))


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

    session_id = generate_session_id()
    user.session_id = session_id
    db.commit()

    return create_access_token({"sub": str(user.id_usuario), "sid": session_id})


def register(data: RegisterRequest, db: Session) -> tuple:
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="El email ya está registrado")

    codigo = _generar_codigo()
    user = Usuario(
        id_junta=data.id_junta,
        id_rol=ROL_VECINO_ID,
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        telefono=data.telefono,
        password_hash=hash_password(data.password),
        email_verificado=False,
        token_verificacion=codigo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    email_enviado = False
    email_error = None
    try:
        from backend.services.email_service import enviar_codigo_verificacion
        enviar_codigo_verificacion(user.email, user.nombre, codigo)
        email_enviado = True
    except Exception as e:
        import sys
        email_error = f"{type(e).__name__}: {e}"
        print(f"[EMAIL ERROR] {email_error}", file=sys.stderr)

    return user, email_enviado, email_error

    return user


def verificar_codigo(email: str, codigo: str, db: Session) -> bool:
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or user.token_verificacion != codigo:
        return False
    user.email_verificado = True
    user.token_verificacion = None
    db.commit()
    return True


def reenviar_codigo(email: str, db: Session) -> tuple:
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or user.email_verificado:
        return False, "Usuario no encontrado o ya verificado"
    codigo = _generar_codigo()
    user.token_verificacion = codigo
    db.commit()
    try:
        from backend.services.email_service import enviar_codigo_verificacion
        enviar_codigo_verificacion(user.email, user.nombre, codigo)
        return True, None
    except Exception as e:
        import sys
        error = f"{type(e).__name__}: {e}"
        print(f"[EMAIL ERROR reenviar] {error}", file=sys.stderr)
        return False, error


def verificar_email(token: str, db: Session) -> bool:
    user = db.query(Usuario).filter(Usuario.token_verificacion == token).first()
    if not user:
        return False
    user.email_verificado = True
    user.token_verificacion = None
    db.commit()
    return True
