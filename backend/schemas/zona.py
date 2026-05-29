from __future__ import annotations
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from backend.models.zona_caliente import NivelRiesgo


class ZonaResponse(BaseModel):
    id_zona: int
    id_junta: int
    nombre: str
    distrito: str | None = None
    latitud_centro: Decimal
    longitud_centro: Decimal
    radio_metros: int
    nivel_riesgo: NivelRiesgo
    total_reportes_30d: int
    ultima_actualizacion: datetime

    model_config = {"from_attributes": True}


class HeatmapPoint(BaseModel):
    lat: float
    lng: float
    intensity: float


