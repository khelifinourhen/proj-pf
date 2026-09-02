import os
"""
Service de Detection d Anomalies IoT Aeronautique
Flask API - Version Production-Ready
PFE 2025/2026

Endpoints :
  GET  /health     -> statut API
  GET  /info       -> metadata modele
  POST /predict    -> prediction anomalie
  POST /predict/batch -> batch prediction
  GET  /scenarios  -> donnees test 3 scenarios
"""
import json
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────
# CHARGEMENT DES ARTEFACTS AU DEMARRAGE
# ──────────────────────────────────────────────────────────
def get_model_dir() -> Path:
    candidates = [
        Path(__file__).parent / "model",
        Path(__file__).parent.parent / "model",
        Path("model"),
        Path(__file__).parent,
    ]
    for c in candidates:
        if (c / "model_pipeline.joblib").exists():
            return c
    return Path(__file__).parent / "model"

MODEL_DIR = get_model_dir()

def load_artifacts():
    pipeline = joblib.load(MODEL_DIR / "model_pipeline.joblib")
    config   = joblib.load(MODEL_DIR / "if_config.joblib")
    with open(MODEL_DIR / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    logger.info(f"Modele charge : {metadata['model']} v{metadata['version']}")
    logger.info(f"Features      : {metadata['n_features']}")
    logger.info(f"Seuil         : {config['threshold']:.6f} (P{config['percentile']})")
    return pipeline, config, metadata

PIPELINE, CONFIG, METADATA = load_artifacts()
FEATURES = METADATA["features"]

START_TIME = datetime.utcnow()
stats = {"predictions": 0, "anomalies": 0}

# ──────────────────────────────────────────────────────────
# APPLICATION FLASK
# ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["JSON_ENSURE_ASCII"] = False


def do_predict(data: dict) -> dict:
    """Effectue la prediction sur un dict de features."""
    row = {f: data.get(f, None) for f in FEATURES}
    X   = pd.DataFrame([row])

    score    = -float(PIPELINE.score_samples(X)[0])
    is_anom  = int(score >= CONFIG["threshold"])
    status   = "ANOMALY" if is_anom else "NORMAL"

    stats["predictions"] += 1
    if is_anom:
        stats["anomalies"] += 1

    logger.info(f"Prediction | score={score:.4f} seuil={CONFIG['threshold']:.4f} -> {status}")

    return {
        "anomaly":       is_anom,
        "anomaly_score": round(score, 6),
        "status":        status,
        "model":         METADATA["model"],
        "threshold":     round(CONFIG["threshold"], 6),
        "timestamp":     datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "message":       f"Anomalie detectee (score={score:.3f})" if is_anom else "Comportement normal"
    }


# ──────────────────────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    uptime = (datetime.utcnow() - START_TIME).total_seconds()
    return jsonify({
        "status":           "ok",
        "model_loaded":     True,
        "model":            METADATA["model"],
        "version":          METADATA["version"],
        "uptime_seconds":   round(uptime, 1),
        "predictions_made": stats["predictions"],
        "anomalies_found":  stats["anomalies"],
        "anomaly_rate":     round(stats["anomalies"] / max(stats["predictions"], 1), 4)
    })


@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "model":                METADATA["model"],
        "version":              METADATA["version"],
        "n_features":           METADATA["n_features"],
        "features":             METADATA["features"],
        "threshold":            CONFIG["threshold"],
        "threshold_percentile": CONFIG["percentile"],
        "contamination":        CONFIG["contamination"],
        "metrics_test":         METADATA.get("metrics_test", {}),
        "training_date":        METADATA.get("training_date"),
        "pipeline_steps":       METADATA.get("pipeline_steps", []),
        "forbidden_features":   METADATA.get("forbidden_features", [])
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "JSON invalide ou Content-Type incorrect"}), 400
    try:
        result = do_predict(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur predict: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    data = request.get_json(silent=True)
    if not data or "readings" not in data:
        return jsonify({"error": "Format attendu: {readings: [...]}"}), 400
    if not data["readings"]:
        return jsonify({"error": "La liste readings est vide"}), 400
    try:
        predictions = [do_predict(r) for r in data["readings"]]
        return jsonify({
            "predictions":        predictions,
            "total":              len(predictions),
            "anomalies_detected": sum(p["anomaly"] for p in predictions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/scenarios", methods=["GET"])
def scenarios():
    return jsonify({
        "scenario_1_nominal": {
            "description": "Vol normal - tous parametres dans les plages nominales",
            "expected":    "NORMAL",
            "data": {
                "temperature_c": 24.5, "pressure_hpa": 1013.0,
                "humidity_pct": 52.0,  "altitude_m": 3000.0,
                "airspeed_kts": 250.0, "vibration_norm_ms2": 0.12,
                "voltage_v": 3.3, "current_a": 0.85, "power_w": 2.8,
                "rpm": 1450.0, "operating_hours": 1200.0,
                "load_pct": 55.0, "motor_current_temp_c": 45.0
            }
        },
        "scenario_2_limite": {
            "description": "Parametres aux limites - surveillance requise",
            "expected":    "NORMAL ou ANOMALY",
            "data": {
                "temperature_c": 68.0, "pressure_hpa": 980.0,
                "humidity_pct": 88.0,  "altitude_m": 9500.0,
                "airspeed_kts": 420.0, "vibration_norm_ms2": 1.8,
                "voltage_v": 3.1, "current_a": 1.9, "power_w": 5.9,
                "rpm": 2800.0, "operating_hours": 4800.0, "load_pct": 89.0
            }
        },
        "scenario_3_anomalie": {
            "description": "Anomalie detectee - surchauffe et vibrations critiques",
            "expected":    "ANOMALY",
            "data": {
                "temperature_c": 142.0, "pressure_hpa": 650.0,
                "humidity_pct": 98.0,   "altitude_m": 12000.0,
                "airspeed_kts": 580.0,  "vibration_norm_ms2": 15.3,
                "voltage_v": 2.4, "current_a": 4.8, "power_w": 11.5,
                "rpm": 5500.0, "operating_hours": 8900.0,
                "motor_current_temp_c": 148.0
            }
        }
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint introuvable", "available": ["/health", "/info", "/predict", "/predict/batch", "/scenarios"]}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Methode non autorisee"}), 405


if __name__ == "__main__":
    logger.info("Demarrage du service Flask sur http://0.0.0.0:5000")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

