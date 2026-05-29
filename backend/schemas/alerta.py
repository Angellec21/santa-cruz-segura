from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from backend.models.alerta import TipoAlerta, EstadoAlerta


class AlertaCreate(BaseModel):
    id_zona: int
    id_junta: int
    titulo: str
    descripcion: str | None = None
    tipo: TipoAlerta
    fecha_fin: datetime | None = None


class AlertaResponse(BaseModel):
    id_alerta: int
    id_zona: int
    id_junta: int
    id_creador: int
    titulo: str
    descripcion: str | None
    tipo: TipoAlerta
    estado: EstadoAlerta
    fecha_inicio: datetime
    fecha_fin: datetime | None

    model_config = {"from_attributes": True}
