from __future__ import annotations
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str | None = None
    password: str
    id_junta: int
