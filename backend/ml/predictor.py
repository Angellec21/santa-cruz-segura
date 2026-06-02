import os
import pickle
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.pkl"


class Predictor:
    def __init__(self):
        self._model = None

    def _load(self):
        if self._model is None and MODEL_PATH.exists():
            with open(MODEL_PATH, "rb") as f:
                self._model = pickle.load(f)

    def predict(self, features: dict) -> tuple[str, float]:
        self._load()
        if self._model is None:
            return self._heuristica(features)

        nivel_map = {0: "bajo", 1: "medio", 2: "alto", 3: "critico"}
        X = [[features.get("total_reportes_30d", 0)]]
        pred = self._model.predict(X)[0]
        proba = max(self._model.predict_proba(X)[0])
        return nivel_map.get(pred, "bajo"), round(proba, 4)

    def _heuristica(self, features: dict) -> tuple[str, float]:
        """
        Combina reportes de los últimos 30 días con el nivel de riesgo
        actual para generar una predicción coherente a 7 días.
        - 50% peso en tendencia de reportes
        - 50% peso en nivel actual (zones con historial de riesgo mantienen alerta)
        """
        n = features.get("total_reportes_30d", 0)
        nivel_actual = features.get("nivel_riesgo_actual", "bajo")
        nivel_map = {"bajo": 0, "medio": 1, "alto": 2, "critico": 3}
        nivel_inv = {0: "bajo", 1: "medio", 2: "alto", 3: "critico"}
        nivel_num = nivel_map.get(nivel_actual, 0)

        # Score basado en reportes (0-3)
        if n >= 15:
            rep_score = 3
        elif n >= 8:
            rep_score = 2
        elif n >= 3:
            rep_score = 1
        else:
            rep_score = 0

        # Promedio ponderado: 50% reportes + 50% nivel actual
        final_score = (rep_score * 0.5) + (nivel_num * 0.5)
        final_level = nivel_inv[min(3, round(final_score))]

        # Confianza: mayor si reportes y nivel actual coinciden
        consistency = 1.0 - abs(rep_score - nivel_num) / 3.0
        confidence = round(0.62 + consistency * 0.28, 2)

        return final_level, confidence


predictor = Predictor()
