from __future__ import annotations
from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str | None
    id_junta: int
    id_rol: int
    activo: bool
    latitud: Decimal | None
    longitud: Decimal | None
    fecha_registro: datetime

    model_config = {"from_attributes": True}


class UsuarioEstadoUpdate(BaseModel):
    activo: bool
