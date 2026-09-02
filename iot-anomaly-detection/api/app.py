"""
API FastAPI - Service de Detection d'Anomalies IoT Aeronautique
Projet PFE 2025/2026

Endpoints :
  GET  /health   -> status de l'API
  GET  /info     -> metadata du modele
  POST /predict  -> prediction d'anomalie
  POST /predict/batch -> prediction sur plusieurs observations
"""
import json
import time
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

import numpy as np
import pandas as pd
import joblib

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from contextlib import asynccontextmanager

# ──────────────────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────
# CHARGEMENT DES ARTEFACTS
# ──────────────────────────────────────────────────────────
MODEL_DIR = Path(__file__).parent.parent / "model"

def load_artifacts():
    """Charge le pipeline et la configuration au demarrage."""
    pipeline_path = MODEL_DIR / "model_pipeline.joblib"
    config_path   = MODEL_DIR / "if_config.joblib"
    meta_path     = MODEL_DIR / "metadata.json"

    if not pipeline_path.exists():
        raise FileNotFoundError(f"model_pipeline.joblib introuvable dans {MODEL_DIR}")

    pipeline = joblib.load(pipeline_path)
    config   = joblib.load(config_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    logger.info(f"Modele charge : {metadata['model']} v{metadata['version']}")
    logger.info(f"Features      : {metadata['n_features']}")
    logger.info(f"Seuil         : {config['threshold']:.6f} (P{config['percentile']})")
    return pipeline, config, metadata

# ──────────────────────────────────────────────────────────
# STARTUP / SHUTDOWN
# ──────────────────────────────────────────────────────────
pipeline = None
config   = None
metadata = None
start_time = datetime.utcnow()
prediction_count = 0
anomaly_count    = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline, config, metadata
    logger.info("Demarrage de l'API ML...")
    pipeline, config, metadata = load_artifacts()
    logger.info("API prete.")
    yield
    logger.info("Arret de l'API.")

# ──────────────────────────────────────────────────────────
# APPLICATION FASTAPI
# ──────────────────────────────────────────────────────────
app = FastAPI(
    title="IoT Anomaly Detection API",
    description="Service de detection d anomalies pour monitoring aeronautique (PFE 2025/2026)",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────
# SCHEMAS PYDANTIC
# ──────────────────────────────────────────────────────────
class SensorReading(BaseModel):
    """Donnees capteurs provenant de l ESP32 via Node-RED."""
    # Capteurs environnementaux
    ambient_temp_c:           Optional[float] = None
    humidity_pct:             Optional[float] = None
    altitude_m:               Optional[float] = None
    airspeed_kts:             Optional[float] = None
    # Parametres operationnels
    load_pct:                 Optional[float] = None
    operating_hours:          Optional[float] = None
    flight_cycle_count:       Optional[float] = None
    cycles_since_maintenance: Optional[float] = None
    maintenance_age_days:     Optional[float] = None
    # Capteurs physiques principaux
    temperature_c:            Optional[float] = None
    atmospheric_pressure_hpa: Optional[float] = None
    pressure_hpa:             Optional[float] = None
    vibration_x_ms2:          Optional[float] = None
    vibration_y_ms2:          Optional[float] = None
    vibration_z_ms2:          Optional[float] = None
    vibration_norm_ms2:       Optional[float] = None
    # Capteurs electriques
    voltage_v:                Optional[float] = None
    current_a:                Optional[float] = None
    power_w:                  Optional[float] = None
    energy_wh_interval:       Optional[float] = None
    # Moteur
    rpm:                      Optional[float] = None
    motor_current_temp_c:     Optional[float] = None
    # Connectivite IoT
    wifi_rssi_dbm:            Optional[float] = None
    packet_latency_ms:        Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "temperature_c": 25.4,
                "pressure_hpa": 1012.5,
                "humidity_pct": 55.0,
                "vibration_norm_ms2": 0.15,
                "voltage_v": 3.3,
                "current_a": 0.85,
                "power_w": 2.8,
                "rpm": 1450.0,
                "operating_hours": 1200.0
            }
        }

class PredictionResponse(BaseModel):
    anomaly:       int
    anomaly_score: float
    status:        str
    model:         str
    threshold:     float
    timestamp:     str
    message:       Optional[str] = None

class BatchRequest(BaseModel):
    readings: list[SensorReading]

class BatchResponse(BaseModel):
    predictions: list[PredictionResponse]
    total: int
    anomalies_detected: int

# ──────────────────────────────────────────────────────────
# FONCTION UTILITAIRE
# ──────────────────────────────────────────────────────────
def predict_single(reading: SensorReading) -> dict:
    """Effectue la prediction sur une seule observation."""
    global prediction_count, anomaly_count

    # Construction du DataFrame avec les features dans le bon ordre
    features = metadata["features"]
    row = {f: getattr(reading, f, None) for f in features}
    X = pd.DataFrame([row])

    # Inference
    score    = -float(pipeline.score_samples(X)[0])
    is_anom  = int(score >= config["threshold"])
    status   = "ANOMALY" if is_anom else "NORMAL"

    prediction_count += 1
    if is_anom:
        anomaly_count += 1

    logger.info(f"Prediction: score={score:.4f} seuil={config['threshold']:.4f} -> {status}")

    return {
        "anomaly":       is_anom,
        "anomaly_score": round(score, 6),
        "status":        status,
        "model":         metadata["model"],
        "threshold":     round(config["threshold"], 6),
        "timestamp":     datetime.utcnow().isoformat() + "Z",
        "message":       f"Anomalie detectee (score={score:.3f})" if is_anom else "Comportement normal"
    }

# ──────────────────────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    """Verification du statut de l API."""
    uptime = (datetime.utcnow() - start_time).total_seconds()
    return {
        "status":           "ok",
        "model_loaded":     pipeline is not None,
        "uptime_seconds":   round(uptime, 1),
        "predictions_made": prediction_count,
        "anomalies_found":  anomaly_count,
        "anomaly_rate":     round(anomaly_count / max(prediction_count, 1), 4)
    }

@app.get("/info")
async def info():
    """Informations sur le modele charge."""
    if metadata is None:
        raise HTTPException(status_code=503, detail="Modele non charge")
    return {
        "model":              metadata["model"],
        "version":            metadata["version"],
        "n_features":         metadata["n_features"],
        "features":           metadata["features"],
        "threshold":          config["threshold"],
        "threshold_percentile": config["percentile"],
        "contamination":      config["contamination"],
        "metrics_test":       metadata.get("metrics_test", {}),
        "training_date":      metadata.get("training_date"),
        "pipeline_steps":     metadata.get("pipeline_steps", [])
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(reading: SensorReading):
    """
    Predit si une observation est une anomalie.
    
    Recoit les mesures capteurs de l ESP32 via Node-RED.
    Retourne: anomaly (0/1), anomaly_score, status (NORMAL/ANOMALY).
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Modele non disponible")
    try:
        result = predict_single(reading)
        return result
    except Exception as e:
        logger.error(f"Erreur prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.post("/predict/batch", response_model=BatchResponse)
async def predict_batch(batch: BatchRequest):
    """Prediction sur un lot d observations."""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Modele non disponible")
    if not batch.readings:
        raise HTTPException(status_code=400, detail="La liste readings est vide")
    try:
        predictions = [predict_single(r) for r in batch.readings]
        n_anom = sum(p["anomaly"] for p in predictions)
        return {
            "predictions":        predictions,
            "total":              len(predictions),
            "anomalies_detected": n_anom
        }
    except Exception as e:
        logger.error(f"Erreur batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scenarios")
async def scenarios():
    """Donnees de test pour les 3 scenarios de demonstration."""
    return {
        "scenario_1_nominal": {
            "description": "Vol normal - tous parametres dans les plages nominales",
            "data": {
                "temperature_c": 24.5, "pressure_hpa": 1013.0,
                "humidity_pct": 52.0, "altitude_m": 3000.0,
                "airspeed_kts": 250.0, "vibration_norm_ms2": 0.12,
                "voltage_v": 3.3, "current_a": 0.85, "power_w": 2.8,
                "rpm": 1450.0, "operating_hours": 1200.0,
                "load_pct": 55.0, "motor_current_temp_c": 45.0,
                "wifi_rssi_dbm": -65.0, "packet_latency_ms": 12.0
            }
        },
        "scenario_2_limite": {
            "description": "Parametres aux limites - surveillance requise",
            "data": {
                "temperature_c": 68.0, "pressure_hpa": 980.0,
                "humidity_pct": 88.0, "altitude_m": 9500.0,
                "airspeed_kts": 420.0, "vibration_norm_ms2": 1.8,
                "voltage_v": 3.1, "current_a": 1.9, "power_w": 5.9,
                "rpm": 2800.0, "operating_hours": 4800.0,
                "load_pct": 89.0, "motor_current_temp_c": 88.0,
                "wifi_rssi_dbm": -85.0, "packet_latency_ms": 95.0
            }
        },
        "scenario_3_anomalie": {
            "description": "Anomalie detectee - surchauffe et vibrations critiques",
            "data": {
                "temperature_c": 142.0, "pressure_hpa": 650.0,
                "humidity_pct": 98.0, "altitude_m": 12000.0,
                "airspeed_kts": 580.0, "vibration_norm_ms2": 15.3,
                "voltage_v": 2.4, "current_a": 4.8, "power_w": 11.5,
                "rpm": 5500.0, "operating_hours": 8900.0,
                "load_pct": 97.0, "motor_current_temp_c": 148.0,
                "wifi_rssi_dbm": -95.0, "packet_latency_ms": 380.0
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=False, log_level="info")
