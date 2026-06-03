from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from backend.models.reporte import EstadoReporte


class EvidenciaResponse(BaseModel):
    id_evidencia: int
    tipo_archivo: str
    ruta_archivo: str
    nombre_original: Optional[str] = None

    model_config = {"from_attributes": True}


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
    tipo_nombre: Optional[str] = None
    zona_nombre: Optional[str] = None
    reporter_nombre: Optional[str] = None
    reporter_apellido: Optional[str] = None
    id_autoridad: Optional[int] = None
    autoridad_nombre: Optional[str] = None
    evidencias: list[EvidenciaResponse] = []


class IncidenteResponse(ReporteGestionResponse):
    distancia_metros: Optional[float] = None
