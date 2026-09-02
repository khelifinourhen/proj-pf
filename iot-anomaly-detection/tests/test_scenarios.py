"""
Test rapide du service ML - sans serveur FastAPI
Simule les 3 scenarios de demonstration
"""
import sys
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(r"c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection\model")

print("=" * 65)
print("TEST RAPIDE DU PIPELINE ML - 3 SCENARIOS")
print("=" * 65)

# Chargement
print("\nChargement du modele...")
try:
    pipeline = joblib.load(MODEL_DIR / "model_pipeline.joblib")
    config   = joblib.load(MODEL_DIR / "if_config.joblib")
    with open(MODEL_DIR / "metadata.json", "r") as f:
        meta = json.load(f)
    print(f"  Modele     : {meta['model']} v{meta['version']}")
    print(f"  Features   : {meta['n_features']}")
    print(f"  Seuil      : {config['threshold']:.6f} (P{config['percentile']})")
    print(f"  ROC-AUC    : {meta['metrics_test']['roc_auc']}")
except Exception as e:
    print(f"ERREUR chargement: {e}")
    sys.exit(1)

FEATURES = meta["features"]

def predict(data: dict, label: str):
    row = {f: data.get(f, None) for f in FEATURES}
    X = pd.DataFrame([row])
    score   = -float(pipeline.score_samples(X)[0])
    is_anom = int(score >= config["threshold"])
    status  = "ANOMALY" if is_anom else "NORMAL"
    icon    = "ALERTE" if is_anom else "OK"
    print(f"\n  [{label}]")
    print(f"    Score d anomalie : {score:.6f}")
    print(f"    Seuil            : {config['threshold']:.6f}")
    print(f"    Anomalie         : {is_anom}")
    print(f"    Statut           : {status}  [{icon}]")
    return {"anomaly": is_anom, "score": score, "status": status}

# === SCENARIO 1 : NOMINAL ===
print("\n" + "-" * 65)
print("SCENARIO 1 - VOL NOMINAL (toutes valeurs normales)")
print("-" * 65)
r1 = predict({
    "temperature_c": 24.5, "pressure_hpa": 1013.0,
    "humidity_pct": 52.0, "altitude_m": 3000.0,
    "airspeed_kts": 250.0, "vibration_norm_ms2": 0.12,
    "voltage_v": 3.3, "current_a": 0.85, "power_w": 2.8,
    "rpm": 1450.0, "operating_hours": 1200.0,
    "load_pct": 55.0, "motor_current_temp_c": 45.0,
    "wifi_rssi_dbm": -65.0, "packet_latency_ms": 12.0
}, "NOMINAL")

# === SCENARIO 2 : LIMITE ===
print("\n" + "-" * 65)
print("SCENARIO 2 - PARAMETRES AUX LIMITES (surveillance requise)")
print("-" * 65)
r2 = predict({
    "temperature_c": 68.0, "pressure_hpa": 980.0,
    "humidity_pct": 88.0, "altitude_m": 9500.0,
    "airspeed_kts": 420.0, "vibration_norm_ms2": 1.8,
    "voltage_v": 3.1, "current_a": 1.9, "power_w": 5.9,
    "rpm": 2800.0, "operating_hours": 4800.0,
    "load_pct": 89.0, "motor_current_temp_c": 88.0,
    "wifi_rssi_dbm": -85.0, "packet_latency_ms": 95.0
}, "LIMITE")

# === SCENARIO 3 : ANOMALIE ===
print("\n" + "-" * 65)
print("SCENARIO 3 - ANOMALIE DETECTEE (surchauffe + vibrations critiques)")
print("-" * 65)
r3 = predict({
    "temperature_c": 142.0, "pressure_hpa": 650.0,
    "humidity_pct": 98.0, "altitude_m": 12000.0,
    "airspeed_kts": 580.0, "vibration_norm_ms2": 15.3,
    "voltage_v": 2.4, "current_a": 4.8, "power_w": 11.5,
    "rpm": 5500.0, "operating_hours": 8900.0,
    "load_pct": 97.0, "motor_current_temp_c": 148.0,
    "wifi_rssi_dbm": -95.0, "packet_latency_ms": 380.0
}, "ANOMALIE")

# === RESUME ===
print("\n" + "=" * 65)
print("RESUME DES 3 SCENARIOS")
print("=" * 65)
print(f"  Scenario 1 NOMINAL  : score={r1['score']:.4f} | {r1['status']}")
print(f"  Scenario 2 LIMITE   : score={r2['score']:.4f} | {r2['status']}")
print(f"  Scenario 3 ANOMALIE : score={r3['score']:.4f} | {r3['status']}")
print(f"  Seuil de detection  : {config['threshold']:.4f}")
print("\nLe pipeline ML est pret pour le deploiement.")
