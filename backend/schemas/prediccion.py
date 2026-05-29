from __future__ import annotations
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal


class PrediccionResponse(BaseModel):
    id_prediccion: int
    id_zona: int
    periodo_inicio: date
    periodo_fin: date
    nivel_predicho: str
    probabilidad: Decimal | None
    fecha_generacion: datetime

    model_config = {"from_attributes": True}
