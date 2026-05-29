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
        n = features.get("total_reportes_30d", 0)
        if n >= 20:
            return "critico", 0.90
        elif n >= 10:
            return "alto", 0.75
        elif n >= 5:
            return "medio", 0.60
        return "bajo", 0.85


predictor = Predictor()
