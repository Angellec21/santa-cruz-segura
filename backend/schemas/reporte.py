from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from backend.models.reporte import EstadoReporte


class ReporteCreate(BaseModel):
    id_zona: int
    id_tipo: int
    descripcion: str | None = None
    latitud: Decimal
    longitud: Decimal
    anonimo: bool = False
    fecha_incidente: datetime


class ReporteResponse(BaseModel):
    id_reporte: int
    id_usuario: int
    id_zona: int
    id_tipo: int
    descripcion: str | None
    latitud: Decimal
    longitud: Decimal
    estado: EstadoReporte
    anonimo: bool
    fecha_incidente: datetime
    fecha_reporte: datetime

    model_config = {"from_attributes": True}


class ReporteEstadoUpdate(BaseModel):
    estado: EstadoReporte


class ReporteGestionResponse(ReporteResponse):
    """Respuesta extendida para directivo/autoridad/admin con info del reportante."""
    tipo_nombre: Optional[str] = None
    zona_nombre: Optional[str] = None
    reporter_nombre: Optional[str] = None    # siempre visible para admin
    reporter_apellido: Optional[str] = None  # siempre visible para admin
