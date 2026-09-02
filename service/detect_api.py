# service/detect_api.py
"""
FastAPI service that loads the IsolationForest model and preprocessing pipeline
and exposes a `/predict` endpoint. The model and preprocessing artefacts are
stored in the sibling `../model/` directory.

Expected input JSON keys must match the numeric features used during training.
"""

import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# The model directory is one level up from the service folder
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

# ---------------------------------------------------------------------
# Load artefacts once at startup
# ---------------------------------------------------------------------
try:
    if_model = joblib.load(os.path.join(MODEL_DIR, "isolation_forest_model.joblib"))
    preprocess = joblib.load(os.path.join(MODEL_DIR, "preprocess_pipeline.joblib"))
    config = joblib.load(os.path.join(MODEL_DIR, "if_config.joblib"))
    numeric_features = joblib.load(os.path.join(MODEL_DIR, "numeric_features.joblib"))
except Exception as exc:
    raise RuntimeError(f"Failed to load model artefacts: {exc}") from exc

imputer = preprocess["imputer"]
scaler = preprocess["scaler"]
# pca = preprocess.get("pca")   # Décommentez si vous avez sauvegardé une étape PCA

# ---------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------
app = FastAPI(title="Anomaly‑Detection API", version="1.0")

# ---------------------------------------------------------------------
# Input schema – must contain exactly the numeric features used at train time
# ---------------------------------------------------------------------
class Measurement(BaseModel):
    ambient_temp_c: float
    humidity_pct: float
    altitude_m: float
    airspeed_kts: float
    load_pct: float
    operating_hours: float
    flight_cycle_count: int
    cycles_since_maintenance: int
    maintenance_age_days: int
    temperature_c: float
    atmospheric_pressure_hpa: float
    pressure_hpa: float
    vibration_x_ms2: float
    vibration_y_ms2: float
    vibration_z_ms2: float
    vibration_norm_ms2: float
    voltage_v: float
    current_a: float
    power_w: float
    energy_wh_interval: float

# ---------------------------------------------------------------------
# Helper: convert Measurement instance to ordered numpy array
# ---------------------------------------------------------------------
def measurement_to_array(meas: Measurement) -> np.ndarray:
    # Preserve the order that was stored in numeric_features during training
    ordered_values = [getattr(meas, name) for name in numeric_features]
    return np.array(ordered_values).reshape(1, -1)

# ---------------------------------------------------------------------
# /predict endpoint
# ---------------------------------------------------------------------
@app.post("/predict")
def predict(meas: Measurement):
    # 1️⃣ Convert JSON payload to the matrix expected by the pipeline
    X = measurement_to_array(meas)

    # 2️⃣ Apply the same preprocessing steps that were used during training
    X_imp = imputer.transform(X)
    X_sc = scaler.transform(X_imp)
    # if pca is not None:
    #     X_sc = pca.transform(X_sc)

    # 3️⃣ Compute the anomaly score (IsolationForest returns higher scores for normal points)
    score = -float(if_model.score_samples(X_sc)[0])
    is_anomaly = score >= config["threshold"]

    return {
        "anomaly": int(is_anomaly),   # 0 = normal, 1 = anomaly
        "score": round(score, 4),
        "threshold": round(config["threshold"], 4),
        "status": "ok",
    }

# ---------------------------------------------------------------------
# Optional health‑check endpoint
# ---------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "alive"}
