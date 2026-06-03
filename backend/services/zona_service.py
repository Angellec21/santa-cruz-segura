from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models.zona_caliente import ZonaCaliente
from backend.models.reporte import Reporte
from backend.schemas.zona import HeatmapPoint, ZonaResponse


def listar_zonas(db: Session) -> list[ZonaResponse]:
    rows = db.execute(text("""
        SELECT z.id_zona, z.id_junta, z.nombre,
               j.distrito,
               z.latitud_centro, z.longitud_centro, z.radio_metros,
               z.nivel_riesgo, z.total_reportes_30d, z.ultima_actualizacion
        FROM zona_caliente z
        LEFT JOIN junta_vecinal j ON j.id_junta = z.id_junta
        ORDER BY j.distrito, z.nombre
    """)).mappings().all()
    return [ZonaResponse(**dict(r)) for r in rows]


def heatmap_zona(id_zona: int, db: Session) -> list[HeatmapPoint]:
    reportes = (
        db.query(Reporte.latitud, Reporte.longitud)
        .filter(
            Reporte.id_zona == id_zona,
            Reporte.estado.notin_(["resuelto", "descartado"]),
        )
        .all()
    )
    intensidad_map = {"bajo": 0.3, "medio": 0.5, "alto": 0.8, "critico": 1.0}
    zona = db.query(ZonaCaliente).filter(ZonaCaliente.id_zona == id_zona).first()
    intensidad = intensidad_map.get(zona.nivel_riesgo.value if zona else "bajo", 0.5)

    return [
        HeatmapPoint(lat=float(r.latitud), lng=float(r.longitud), intensity=intensidad)
        for r in reportes
    ]
