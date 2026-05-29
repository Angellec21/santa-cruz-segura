"""
Script de entrenamiento — ejecutar directamente, no desde uvicorn.
Uso: python backend/ml/train.py
"""
import pickle
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(__file__).parent / "model.pkl"

# Datos sintéticos: feature = total_reportes_30d, label = nivel (0=bajo..3=critico)
np.random.seed(42)
X = np.concatenate([
    np.random.randint(0, 5, 200).reshape(-1, 1),
    np.random.randint(5, 10, 150).reshape(-1, 1),
    np.random.randint(10, 20, 100).reshape(-1, 1),
    np.random.randint(20, 50, 50).reshape(-1, 1),
])
y = np.concatenate([
    np.zeros(200, dtype=int),
    np.ones(150, dtype=int),
    np.full(100, 2, dtype=int),
    np.full(50, 3, dtype=int),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.3f}")

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print(f"Modelo guardado en {MODEL_PATH}")
