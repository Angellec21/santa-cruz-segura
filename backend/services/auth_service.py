from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.usuario import Usuario
from backend.schemas.auth import RegisterRequest
from backend.utils.security import hash_password, verify_password, create_access_token

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
    return create_access_token({"sub": str(user.id_usuario)})


def register(data: RegisterRequest, db: Session) -> Usuario:
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="El email ya está registrado")

    user = Usuario(
        id_junta=data.id_junta,
        id_rol=ROL_VECINO_ID,
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        telefono=data.telefono,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
