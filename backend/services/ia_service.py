from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date, timedelta
from backend.models.zona_caliente import ZonaCaliente
from backend.models.prediccion_ia import PrediccionIA
from backend.ml.predictor import predictor


def predecir_zona(id_zona: int, db: Session) -> PrediccionIA:
    zona = db.query(ZonaCaliente).filter(ZonaCaliente.id_zona == id_zona).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    features = {
        "total_reportes_30d": zona.total_reportes_30d,
        "nivel_riesgo_actual": zona.nivel_riesgo.value,
    }
    nivel_predicho, probabilidad = predictor.predict(features)

    prediccion = PrediccionIA(
        id_zona=id_zona,
        periodo_inicio=date.today(),
        periodo_fin=date.today() + timedelta(days=7),
        nivel_predicho=nivel_predicho,
        probabilidad=probabilidad,
        features_json=str(features),
    )
    db.add(prediccion)
    db.commit()
    db.refresh(prediccion)
    return prediccion
