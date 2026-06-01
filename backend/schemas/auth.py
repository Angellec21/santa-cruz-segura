from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    password: str
    id_junta: int
