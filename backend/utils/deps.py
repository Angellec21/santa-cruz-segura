from __future__ import annotations
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from backend.database import SessionLocal
from backend.models.usuario import Usuario
from backend.utils.security import decode_token

ROL_VECINO = "vecino"
ROL_DIRECTIVO = "directivo"
ROL_AUTORIDAD = "autoridad"
ROL_ADMIN = "admin"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
    if not user or not user.activo:
        raise credentials_error
    return user


def require_role(roles: list[str]):
    def checker(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.rol.nombre not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes",
            )
        return current_user
    return checker
