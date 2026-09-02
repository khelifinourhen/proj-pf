"""
ETAPE 1 -- Entrainement du Pipeline Final et Sauvegarde
Projet PFE : Detection anomalies IoT Aeronautique
Executer avec : F:\ml_env\venv\Scripts\python.exe train_and_save_pipeline.py
"""
import sys, os, json, warnings
import numpy as np
import pandas as pd
from pathlib import Path
import joblib
warnings.filterwarnings("ignore")

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score, confusion_matrix
)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

CSV_PATH  = Path(r"c:\Users\hp\Desktop\Proj pf\aeronautical_iot_esp32_predictive_maintenance_200k (1).csv")
MODEL_DIR = Path(r"c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection\model")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

TARGET_ANOMALIE = "anomaly_reference"
THRESHOLD_PERCENTILE = 95

FEATURES = [
    "ambient_temp_c","humidity_pct","altitude_m","airspeed_kts",
    "load_pct","operating_hours","flight_cycle_count","cycles_since_maintenance",
    "maintenance_age_days","temperature_c","atmospheric_pressure_hpa","pressure_hpa",
    "vibration_x_ms2","vibration_y_ms2","vibration_z_ms2","vibration_norm_ms2",
    "voltage_v","current_a","power_w","energy_wh_interval",
    "rpm","motor_current_temp_c","wifi_rssi_dbm","packet_latency_ms"
]

print("=" * 60)
print("PIPELINE ML -- ENTRAINEMENT ET SAUVEGARDE")
print("=" * 60)

print("\n[1/7] Chargement du dataset...")
df = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
df = df.drop_duplicates().reset_index(drop=True)
print(f"  Shape apres dedup : {df.shape}")

print("\n[2/7] Split temporel 60/20/20...")
n = len(df)
n_train = int(n * 0.60)
n_val   = int(n * 0.20)
df_train = df.iloc[:n_train].copy()
df_val   = df.iloc[n_train:n_train+n_val].copy()
df_test  = df.iloc[n_train+n_val:].copy()
print(f"  TRAIN:{len(df_train)} | VAL:{len(df_val)} | TEST:{len(df_test)}")

FEATURES = [f for f in FEATURES if f in df.columns]
print(f"\n[3/7] Features : {len(FEATURES)}")

X_train = df_train[FEATURES]
X_val   = df_val[FEATURES]
X_test  = df_test[FEATURES]
y_train_ano = df_train[TARGET_ANOMALIE].values
y_val_ano   = df_val[TARGET_ANOMALIE].values
y_test_ano  = df_test[TARGET_ANOMALIE].values

contamination = float(y_train_ano.mean())
print(f"  Contamination TRAIN : {contamination:.4f}")

print("\n[4/7] Construction du Pipeline Sklearn...")
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler",  StandardScaler()),
    ("model",   IsolationForest(
        n_estimators=200,
        contamination=contamination,
        max_samples="auto",
        random_state=RANDOM_STATE,
        n_jobs=-1
    ))
])
pipeline.fit(X_train)
print("  Pipeline.fit(X_train) OK")

print("\n[5/7] Seuil sur VAL normaux P95...")
val_scores = -pipeline.score_samples(X_val)
threshold  = float(np.percentile(val_scores[y_val_ano == 0], THRESHOLD_PERCENTILE))
print(f"  Seuil P{THRESHOLD_PERCENTILE} : {threshold:.6f}")

print("\n[6/7] Evaluation sur TEST...")
test_scores = -pipeline.score_samples(X_test)
test_pred   = (test_scores >= threshold).astype(int)
acc  = accuracy_score(y_test_ano, test_pred)
prec = precision_score(y_test_ano, test_pred, zero_division=0)
rec  = recall_score(y_test_ano, test_pred, zero_division=0)
f1   = f1_score(y_test_ano, test_pred, zero_division=0)
roc  = roc_auc_score(y_test_ano, test_scores)
pr   = average_precision_score(y_test_ano, test_scores)
cm   = confusion_matrix(y_test_ano, test_pred)
tn,fp,fn,tp = cm.ravel()
print(f"  Accuracy={acc:.4f} Precision={prec:.4f} Recall={rec:.4f} F1={f1:.4f} ROC-AUC={roc:.4f}")
print(f"  TN={tn} FP={fp} FN={fn} TP={tp}")

print("\n[7/7] Sauvegarde...")
joblib.dump(pipeline, MODEL_DIR / "model_pipeline.joblib")
joblib.dump({"threshold": threshold, "percentile": THRESHOLD_PERCENTILE, "contamination": contamination}, MODEL_DIR / "if_config.joblib")

metadata = {
    "model": "IsolationForest",
    "version": "2.0",
    "pipeline_steps": ["SimpleImputer(median)", "StandardScaler", "IsolationForest"],
    "n_estimators": 200,
    "random_state": RANDOM_STATE,
    "threshold": threshold,
    "threshold_percentile": THRESHOLD_PERCENTILE,
    "contamination": contamination,
    "features": FEATURES,
    "n_features": len(FEATURES),
    "target": TARGET_ANOMALIE,
    "dataset": "aeronautical_iot_esp32_predictive_maintenance_200k",
    "split": {"train": 0.60, "val": 0.20, "test": 0.20},
    "train_size": len(df_train),
    "metrics_test": {
        "accuracy": round(acc,4), "precision": round(prec,4),
        "recall": round(rec,4), "f1": round(f1,4),
        "roc_auc": round(roc,4), "pr_auc": round(pr,4),
        "confusion_matrix": {"tn": int(tn),"fp": int(fp),"fn": int(fn),"tp": int(tp)}
    },
    "forbidden_features": ["fault_injection_level_pct","failure_type","failure_event","anomaly_reference"],
    "training_date": "2026-08-27",
    "sklearn_version": "1.9.0"
}
with open(MODEL_DIR / "metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("  model_pipeline.joblib OK")
print("  metadata.json OK")

print("\n-- TEST RECHARGEMENT --")
loaded = joblib.load(MODEL_DIR / "model_pipeline.joblib")
cfg    = joblib.load(MODEL_DIR / "if_config.joblib")

s_normal = -float(loaded.score_samples(X_test[y_test_ano==0].iloc[[0]])[0])
s_anom   = -float(loaded.score_samples(X_test[y_test_ano==1].iloc[[0]])[0])
print(f"  Normal  : score={s_normal:.4f} anomaly={int(s_normal>=cfg['threshold'])} (attendu=0)")
print(f"  Anomalie: score={s_anom:.4f} anomaly={int(s_anom>=cfg['threshold'])} (attendu=1)")

print("\n" + "=" * 60)
print("PIPELINE SAUVEGARDE AVEC SUCCES")
print("=" * 60)
for f in sorted(MODEL_DIR.iterdir()):
    print(f"  {f.name:<40} {f.stat().st_size/1024:.1f} KB")
