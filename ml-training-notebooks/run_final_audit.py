# -*- coding: utf-8 -*-
"""
=============================================================================
 SCRIPT D'AUDIT ML REPRODUCTIBLE — PFE Nourhen KHELIFI
 Détection d'Anomalies IoT Aéronautique
 YaneCode Digital — Été 2026
=============================================================================
 Ce script exécute l'intégralité du pipeline ML de bout en bout :
   1. Chargement et nettoyage du dataset
   2. Découpage temporel strict 60/20/20
   3. Prétraitement (Imputer + Scaler) FIT exclusivement sur TRAIN
   4. Entraînement des 4 modèles (IF, OCSVM, LSTM AE, RF)
   5. Calibration des seuils sur VALIDATION
   6. Évaluation sur TEST
   7. Intervalles de confiance par bootstrap
   8. Export des métriques, figures et artefacts
=============================================================================
 Exécution : python run_final_audit.py
 Environnement : Python 3.10+, scikit-learn>=1.3, tensorflow>=2.12
 Seed : RANDOM_STATE = 42
=============================================================================
"""

import os, sys, json, warnings, hashlib, time
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, precision_recall_curve,
)
import joblib

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense
from tensorflow.keras.callbacks import EarlyStopping

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
#  CONFIGURATION EXPÉRIMENTALE
# ═══════════════════════════════════════════════════════════════

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

TRAIN_RATIO = 0.60
VAL_RATIO   = 0.20
TEST_RATIO  = 0.20

SEQ_LEN    = 30
BATCH_SIZE = 64
EPOCHS     = 30
THRESHOLD_PERCENTILE = 95
PCA_COMPONENTS = 10
BOOTSTRAP_N = 1000

TARGET_SUPERVISÉ = 'failure_within_4h'
TARGET_ANOMALIE  = 'anomaly_reference'

NUMERIC_FEATURES = [
    'ambient_temp_c', 'humidity_pct', 'altitude_m', 'airspeed_kts',
    'load_pct', 'operating_hours', 'flight_cycle_count', 'cycles_since_maintenance',
    'maintenance_age_days', 'temperature_c', 'atmospheric_pressure_hpa', 'pressure_hpa',
    'vibration_x_ms2', 'vibration_y_ms2', 'vibration_z_ms2', 'vibration_norm_ms2',
    'voltage_v', 'current_a', 'power_w', 'energy_wh_interval',
    'rpm', 'motor_current_temp_c', 'wifi_rssi_dbm', 'packet_latency_ms'
]

# Adapter le chemin selon l'environnement
CSV_PATH = Path(r"c:\Users\hp\Desktop\Proj pf\aeronautical_iot_esp32_predictive_maintenance_200k (1).csv")
OUTPUT_DIR = Path(r"c:\Users\hp\Desktop\Proj pf\audit_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("  AUDIT ML REPRODUCTIBLE — PFE Nourhen KHELIFI")
print("=" * 70)
print(f"  Date        : {datetime.now().isoformat()}")
print(f"  Seed        : {RANDOM_STATE}")
print(f"  Output dir  : {OUTPUT_DIR}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 1 — CHARGEMENT ET TRAÇABILITÉ
# ═══════════════════════════════════════════════════════════════

print("\n[1/10] Chargement du dataset...")
with open(CSV_PATH, "rb") as f:
    csv_sha256 = hashlib.sha256(f.read()).hexdigest()
print(f"  SHA-256 : {csv_sha256}")

df = pd.read_csv(CSV_PATH, parse_dates=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)
n_before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
n_dedup = n_before - len(df)
print(f"  Observations brutes : {n_before}")
print(f"  Doublons supprimés  : {n_dedup}")
print(f"  Observations finales: {len(df)}")
print(f"  Période : {df['timestamp'].min()} → {df['timestamp'].max()}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 2 — NETTOYAGE
# ═══════════════════════════════════════════════════════════════

print("\n[2/10] Nettoyage des bornes physiques...")
bounds = {
    'temperature_c': (0, 200),
    'humidity_pct': (0, 100),
    'voltage_v': (0, 35),
    'atmospheric_pressure_hpa': (100, 1100),
    'vibration_norm_ms2': (0, 50),
}
for col, (lo, hi) in bounds.items():
    if col in df.columns:
        n_inv = ((df[col] < lo) | (df[col] > hi)).sum()
        df.loc[(df[col] < lo) | (df[col] > hi), col] = np.nan
        if n_inv > 0:
            print(f"  {col}: {n_inv} hors bornes → NaN")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 3 — DÉCOUPAGE TEMPOREL 60/20/20
# ═══════════════════════════════════════════════════════════════

print("\n[3/10] Split temporel 60/20/20...")
n = len(df)
n_train = int(n * TRAIN_RATIO)
n_val   = int(n * VAL_RATIO)

df_train = df.iloc[:n_train].copy()
df_val   = df.iloc[n_train:n_train+n_val].copy()
df_test  = df.iloc[n_train+n_val:].copy()

print(f"  TRAIN : {len(df_train):>7} obs | {df_train['timestamp'].min()} → {df_train['timestamp'].max()}")
print(f"  VAL   : {len(df_val):>7} obs | {df_val['timestamp'].min()} → {df_val['timestamp'].max()}")
print(f"  TEST  : {len(df_test):>7} obs | {df_test['timestamp'].min()} → {df_test['timestamp'].max()}")
print(f"  max(TRAIN) <= min(VAL) : {df_train['timestamp'].max() <= df_val['timestamp'].min()}")
print(f"  max(VAL) <= min(TEST)  : {df_val['timestamp'].max() <= df_test['timestamp'].min()}")

for name, sub, target in [
    ("Train", df_train, TARGET_ANOMALIE),
    ("Val",   df_val,   TARGET_ANOMALIE),
    ("Test",  df_test,  TARGET_ANOMALIE),
]:
    rate = sub[target].mean()
    print(f"  {name} anomaly rate: {rate*100:.2f}%")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 4 — PRÉTRAITEMENT (FIT SUR TRAIN UNIQUEMENT)
# ═══════════════════════════════════════════════════════════════

print("\n[4/10] Prétraitement...")
NUMERIC_FEATURES = [f for f in NUMERIC_FEATURES if f in df.columns]
print(f"  Features retenues : {len(NUMERIC_FEATURES)}")

imputer = SimpleImputer(strategy='median')
imputer.fit(df_train[NUMERIC_FEATURES])
X_train_imp = imputer.transform(df_train[NUMERIC_FEATURES])
X_val_imp   = imputer.transform(df_val[NUMERIC_FEATURES])
X_test_imp  = imputer.transform(df_test[NUMERIC_FEATURES])

scaler = StandardScaler()
scaler.fit(X_train_imp)
X_train = scaler.transform(X_train_imp)
X_val   = scaler.transform(X_val_imp)
X_test  = scaler.transform(X_test_imp)

y_train_sup = df_train[TARGET_SUPERVISÉ].values
y_val_sup   = df_val[TARGET_SUPERVISÉ].values
y_test_sup  = df_test[TARGET_SUPERVISÉ].values
y_train_ano = df_train[TARGET_ANOMALIE].values
y_val_ano   = df_val[TARGET_ANOMALIE].values
y_test_ano  = df_test[TARGET_ANOMALIE].values

print(f"  X_train: {X_train.shape} | X_val: {X_val.shape} | X_test: {X_test.shape}")
print(f"  Imputer FIT sur TRAIN, Scaler FIT sur TRAIN ✓")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 5 — ISOLATION FOREST
# ═══════════════════════════════════════════════════════════════

print("\n[5/10] Isolation Forest...")
contamination_if = float(y_train_ano.mean())
print(f"  contamination = {contamination_if:.4f}")

if_model = IsolationForest(
    n_estimators=200,
    contamination=contamination_if,
    max_samples='auto',
    random_state=RANDOM_STATE,
    n_jobs=-1
)
if_model.fit(X_train)

if_scores_val  = -if_model.score_samples(X_val)
if_scores_test = -if_model.score_samples(X_test)
threshold_if = float(np.percentile(if_scores_val[y_val_ano == 0], THRESHOLD_PERCENTILE))
print(f"  Seuil P{THRESHOLD_PERCENTILE}: {threshold_if:.6f}")

if_pred_test = (if_scores_test >= threshold_if).astype(int)
cm_if = confusion_matrix(y_test_ano, if_pred_test)
tn, fp, fn, tp = cm_if.ravel()

if_metrics = {
    'Accuracy':  round(accuracy_score(y_test_ano, if_pred_test), 4),
    'Precision': round(precision_score(y_test_ano, if_pred_test, zero_division=0), 4),
    'Recall':    round(recall_score(y_test_ano, if_pred_test, zero_division=0), 4),
    'F1':        round(f1_score(y_test_ano, if_pred_test, zero_division=0), 4),
    'ROC-AUC':   round(roc_auc_score(y_test_ano, if_scores_test), 4),
    'PR-AUC':    round(average_precision_score(y_test_ano, if_scores_test), 4),
    'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp),
}
print(f"  Metrics: {if_metrics}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 6 — ONE-CLASS SVM
# ═══════════════════════════════════════════════════════════════

print("\n[6/10] One-Class SVM...")
pca = PCA(n_components=PCA_COMPONENTS, random_state=RANDOM_STATE)
pca.fit(X_train)
X_train_pca = pca.transform(X_train)
X_val_pca   = pca.transform(X_val)
X_test_pca  = pca.transform(X_test)
print(f"  PCA variance expliquée: {pca.explained_variance_ratio_.sum()*100:.1f}%")

n_svm = min(5000, len(X_train_pca))
idx_svm = np.random.choice(len(X_train_pca), n_svm, replace=False)
ocsvm = OneClassSVM(kernel='rbf', nu=0.1, gamma='scale')
ocsvm.fit(X_train_pca[idx_svm])

ocsvm_scores_val  = -ocsvm.decision_function(X_val_pca)
ocsvm_scores_test = -ocsvm.decision_function(X_test_pca)
threshold_ocsvm = float(np.percentile(ocsvm_scores_val[y_val_ano == 0], THRESHOLD_PERCENTILE))
print(f"  Seuil OCSVM: {threshold_ocsvm:.6f}")

ocsvm_pred_test = (ocsvm_scores_test >= threshold_ocsvm).astype(int)
cm_oc = confusion_matrix(y_test_ano, ocsvm_pred_test)
tn, fp, fn, tp = cm_oc.ravel()

ocsvm_metrics = {
    'Accuracy':  round(accuracy_score(y_test_ano, ocsvm_pred_test), 4),
    'Precision': round(precision_score(y_test_ano, ocsvm_pred_test, zero_division=0), 4),
    'Recall':    round(recall_score(y_test_ano, ocsvm_pred_test, zero_division=0), 4),
    'F1':        round(f1_score(y_test_ano, ocsvm_pred_test, zero_division=0), 4),
    'ROC-AUC':   round(roc_auc_score(y_test_ano, ocsvm_scores_test), 4),
    'PR-AUC':    round(average_precision_score(y_test_ano, ocsvm_scores_test), 4),
    'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp),
}
print(f"  Metrics: {ocsvm_metrics}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 7 — LSTM AUTOENCODER
# ═══════════════════════════════════════════════════════════════

print("\n[7/10] LSTM Autoencoder...")

def make_sequences(X, seq_len):
    return np.array([X[i:i+seq_len] for i in range(len(X)-seq_len+1)])

def make_sequences_labels(X, y, seq_len):
    Xs, ys = [], []
    for i in range(len(X)-seq_len+1):
        Xs.append(X[i:i+seq_len])
        ys.append(y[i+seq_len-1])
    return np.array(Xs), np.array(ys)

X_train_normal = X_train[y_train_ano == 0]
X_train_seq = make_sequences(X_train_normal, SEQ_LEN)
X_val_seq, y_val_seq   = make_sequences_labels(X_val, y_val_ano, SEQ_LEN)
X_test_seq, y_test_seq = make_sequences_labels(X_test, y_test_ano, SEQ_LEN)
print(f"  Seq TRAIN normaux: {X_train_seq.shape}")
print(f"  Seq VAL: {X_val_seq.shape} | Seq TEST: {X_test_seq.shape}")

n_feat = X_train.shape[1]
inp = Input(shape=(SEQ_LEN, n_feat))
enc = LSTM(64, activation='tanh', return_sequences=False)(inp)
rep = RepeatVector(SEQ_LEN)(enc)
dec = LSTM(64, activation='tanh', return_sequences=True)(rep)
out = TimeDistributed(Dense(n_feat))(dec)
ae = Model(inp, out)
ae.compile(optimizer='adam', loss='mse')

es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = ae.fit(X_train_seq, X_train_seq, validation_split=0.1,
                 epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[es], verbose=1)
print(f"  Arrêt à l'époque {len(history.history['loss'])}/{EPOCHS}")

def reconstruction_errors(model, X_seq):
    X_pred = model.predict(X_seq, verbose=0)
    return np.mean(np.mean(np.square(X_seq - X_pred), axis=2), axis=1)

val_errors  = reconstruction_errors(ae, X_val_seq)
test_errors = reconstruction_errors(ae, X_test_seq)

threshold_lstm = float(np.percentile(val_errors[y_val_seq == 0], THRESHOLD_PERCENTILE))
print(f"  Seuil LSTM: {threshold_lstm:.6f}")

lstm_pred_test = (test_errors >= threshold_lstm).astype(int)
cm_lstm = confusion_matrix(y_test_seq, lstm_pred_test)
tn, fp, fn, tp = cm_lstm.ravel()

lstm_metrics = {
    'Accuracy':  round(accuracy_score(y_test_seq, lstm_pred_test), 4),
    'Precision': round(precision_score(y_test_seq, lstm_pred_test, zero_division=0), 4),
    'Recall':    round(recall_score(y_test_seq, lstm_pred_test, zero_division=0), 4),
    'F1':        round(f1_score(y_test_seq, lstm_pred_test, zero_division=0), 4),
    'ROC-AUC':   round(roc_auc_score(y_test_seq, test_errors), 4),
    'PR-AUC':    round(average_precision_score(y_test_seq, test_errors), 4),
    'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp),
}
print(f"  Metrics: {lstm_metrics}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 8 — RANDOM FOREST (SUPERVISÉ)
# ═══════════════════════════════════════════════════════════════

print("\n[8/10] Random Forest (supervisé)...")

# Cross-validation temporelle
tscv = TimeSeriesSplit(n_splits=5)
rf_cv_scores = []
for fold, (tr_idx, val_idx) in enumerate(tscv.split(X_train)):
    rf_tmp = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
    rf_tmp.fit(X_train[tr_idx], y_train_sup[tr_idx])
    f1_fold = f1_score(y_train_sup[val_idx], rf_tmp.predict(X_train[val_idx]), zero_division=0)
    rf_cv_scores.append(f1_fold)
    print(f"  Fold {fold+1}: F1={f1_fold:.4f}")
print(f"  CV F1 moyen: {np.mean(rf_cv_scores):.4f} ± {np.std(rf_cv_scores):.4f}")

rf_model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
rf_model.fit(X_train, y_train_sup)
rf_proba_test = rf_model.predict_proba(X_test)[:, 1]
rf_pred_test  = rf_model.predict(X_test)

cm_rf = confusion_matrix(y_test_sup, rf_pred_test)
tn, fp, fn, tp = cm_rf.ravel()

rf_metrics = {
    'Accuracy':  round(accuracy_score(y_test_sup, rf_pred_test), 4),
    'Precision': round(precision_score(y_test_sup, rf_pred_test, zero_division=0), 4),
    'Recall':    round(recall_score(y_test_sup, rf_pred_test, zero_division=0), 4),
    'F1':        round(f1_score(y_test_sup, rf_pred_test, zero_division=0), 4),
    'ROC-AUC':   round(roc_auc_score(y_test_sup, rf_proba_test), 4),
    'PR-AUC':    round(average_precision_score(y_test_sup, rf_proba_test), 4),
    'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp),
}
print(f"  Metrics: {rf_metrics}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 9 — INTERVALLES DE CONFIANCE (BOOTSTRAP)
# ═══════════════════════════════════════════════════════════════

print(f"\n[9/10] Bootstrap {BOOTSTRAP_N} itérations pour intervalles de confiance...")

def bootstrap_ci(y_true, y_pred, y_scores, n_boot=1000, alpha=0.05, rng_seed=42):
    """Calcule les IC à 95 % par bootstrap pour F1, ROC-AUC, PR-AUC."""
    rng = np.random.RandomState(rng_seed)
    n = len(y_true)
    f1s, rocs, prs = [], [], []
    for _ in range(n_boot):
        idx = rng.choice(n, n, replace=True)
        yt, yp, ys = y_true[idx], y_pred[idx], y_scores[idx]
        if len(np.unique(yt)) < 2:
            continue
        f1s.append(f1_score(yt, yp, zero_division=0))
        rocs.append(roc_auc_score(yt, ys))
        prs.append(average_precision_score(yt, ys))
    return {
        'F1_CI':      [round(np.percentile(f1s, 100*alpha/2), 4), round(np.percentile(f1s, 100*(1-alpha/2)), 4)],
        'ROC-AUC_CI': [round(np.percentile(rocs, 100*alpha/2), 4), round(np.percentile(rocs, 100*(1-alpha/2)), 4)],
        'PR-AUC_CI':  [round(np.percentile(prs, 100*alpha/2), 4), round(np.percentile(prs, 100*(1-alpha/2)), 4)],
    }

ci_if    = bootstrap_ci(y_test_ano, if_pred_test, if_scores_test, BOOTSTRAP_N)
ci_ocsvm = bootstrap_ci(y_test_ano, ocsvm_pred_test, ocsvm_scores_test, BOOTSTRAP_N)
ci_lstm  = bootstrap_ci(y_test_seq, lstm_pred_test, test_errors, BOOTSTRAP_N)
ci_rf    = bootstrap_ci(y_test_sup, rf_pred_test, rf_proba_test, BOOTSTRAP_N)

print(f"  IF    CI: {ci_if}")
print(f"  OCSVM CI: {ci_ocsvm}")
print(f"  LSTM  CI: {ci_lstm}")
print(f"  RF    CI: {ci_rf}")

# ═══════════════════════════════════════════════════════════════
#  ÉTAPE 10 — FIGURES ET EXPORTS
# ═══════════════════════════════════════════════════════════════

print("\n[10/10] Génération des figures et export...")

# --- Matrices de confusion ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
configs = [
    (y_test_ano, if_pred_test,    'Isolation Forest',  'Blues',   axes[0,0]),
    (y_test_ano, ocsvm_pred_test, 'One-Class SVM',     'Greens',  axes[0,1]),
    (y_test_seq, lstm_pred_test,  'LSTM Autoencoder',  'Oranges', axes[1,0]),
    (y_test_sup, rf_pred_test,    'Random Forest',     'Purples', axes[1,1]),
]
for y_true, y_pred, title, cmap, ax in configs:
    cm = confusion_matrix(y_true, y_pred)
    tn_v, fp_v, fn_v, tp_v = cm.ravel()
    disp = ConfusionMatrixDisplay(cm, display_labels=['Normal', 'Anomalie'])
    disp.plot(ax=ax, colorbar=False, cmap=cmap)
    ax.set_title(f"{title}\nTN={tn_v} FP={fp_v} FN={fn_v} TP={tp_v}", fontsize=10)
plt.suptitle('Matrices de Confusion (TEST)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'confusion_matrices_all.png', dpi=150)
plt.close()

# --- Courbes ROC et PR ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
models_eval = [
    ('Isolation Forest', if_scores_test, y_test_ano, 'steelblue'),
    ('One-Class SVM',    ocsvm_scores_test, y_test_ano, 'forestgreen'),
    ('LSTM Autoencoder', test_errors, y_test_seq, 'darkorange'),
    ('Random Forest',    rf_proba_test, y_test_sup, 'purple'),
]
for label, scores, y_true, color in models_eval:
    fpr, tpr, _ = roc_curve(y_true, scores)
    auc_val = roc_auc_score(y_true, scores)
    ax1.plot(fpr, tpr, color=color, lw=2, label=f"{label} (AUC={auc_val:.3f})")
    prec_c, rec_c, _ = precision_recall_curve(y_true, scores)
    pr_auc = average_precision_score(y_true, scores)
    ax2.plot(rec_c, prec_c, color=color, lw=2, label=f"{label} (PR={pr_auc:.3f})")

ax1.plot([0,1],[0,1],'k--',alpha=0.4)
ax1.set_xlabel('FPR'); ax1.set_ylabel('TPR')
ax1.set_title('Courbes ROC'); ax1.legend(fontsize=9); ax1.grid(alpha=0.3)
ax2.set_xlabel('Recall'); ax2.set_ylabel('Precision')
ax2.set_title('Courbes Precision-Recall'); ax2.legend(fontsize=9); ax2.grid(alpha=0.3)
plt.suptitle('Évaluation TEST', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'roc_pr_curves.png', dpi=150)
plt.close()

# --- Barres comparatives ---
fig, ax = plt.subplots(figsize=(10, 5))
results_df = pd.DataFrame({
    'Isolation Forest': if_metrics,
    'One-Class SVM': ocsvm_metrics,
    'LSTM Autoencoder': lstm_metrics,
    'Random Forest': rf_metrics,
}).T
results_df[['F1', 'ROC-AUC', 'PR-AUC', 'Recall', 'Precision']].plot(
    kind='bar', ax=ax, colormap='tab10', width=0.7)
ax.set_title('Comparaison des modèles — Métriques TEST')
ax.set_ylabel('Score'); ax.set_ylim(0, 1.05)
ax.legend(loc='lower right'); ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'comparaison_modeles.png', dpi=150)
plt.close()

# --- Export JSON des métriques ---
export = {
    'execution_date': datetime.now().isoformat(),
    'dataset': {
        'file': str(CSV_PATH.name),
        'sha256': csv_sha256,
        'total_observations': n,
        'duplicates_removed': n_dedup,
    },
    'configuration': {
        'random_state': RANDOM_STATE,
        'train_ratio': TRAIN_RATIO,
        'val_ratio': VAL_RATIO,
        'test_ratio': TEST_RATIO,
        'seq_len': SEQ_LEN,
        'batch_size': BATCH_SIZE,
        'epochs': EPOCHS,
        'threshold_percentile': THRESHOLD_PERCENTILE,
        'pca_components': PCA_COMPONENTS,
        'n_features': len(NUMERIC_FEATURES),
    },
    'partitions': {
        'train': {
            'size': len(df_train),
            'start': str(df_train['timestamp'].min()),
            'end': str(df_train['timestamp'].max()),
            'anomaly_rate': round(df_train[TARGET_ANOMALIE].mean(), 4),
        },
        'val': {
            'size': len(df_val),
            'start': str(df_val['timestamp'].min()),
            'end': str(df_val['timestamp'].max()),
            'anomaly_rate': round(df_val[TARGET_ANOMALIE].mean(), 4),
        },
        'test': {
            'size': len(df_test),
            'start': str(df_test['timestamp'].min()),
            'end': str(df_test['timestamp'].max()),
            'anomaly_rate': round(df_test[TARGET_ANOMALIE].mean(), 4),
        },
    },
    'thresholds': {
        'isolation_forest': threshold_if,
        'ocsvm': threshold_ocsvm,
        'lstm': threshold_lstm,
    },
    'hyperparameters': {
        'isolation_forest': {'n_estimators': 200, 'contamination': contamination_if, 'max_samples': 'auto'},
        'ocsvm': {'kernel': 'rbf', 'nu': 0.1, 'gamma': 'scale', 'pca_components': PCA_COMPONENTS, 'train_subsample': n_svm},
        'lstm': {'seq_len': SEQ_LEN, 'architecture': '64->RV->64->Dense', 'epochs': EPOCHS, 'batch_size': BATCH_SIZE},
        'random_forest': {'n_estimators': 200, 'cv_splits': 5},
    },
    'metrics': {
        'isolation_forest': if_metrics,
        'ocsvm': ocsvm_metrics,
        'lstm': lstm_metrics,
        'random_forest': rf_metrics,
    },
    'confidence_intervals_95': {
        'isolation_forest': ci_if,
        'ocsvm': ci_ocsvm,
        'lstm': ci_lstm,
        'random_forest': ci_rf,
    },
    'artifacts': [
        'confusion_matrices_all.png',
        'roc_pr_curves.png',
        'comparaison_modeles.png',
        'metrics_final.json',
    ],
}

metrics_path = OUTPUT_DIR / 'metrics_final.json'
with open(metrics_path, 'w', encoding='utf-8') as f:
    json.dump(export, f, ensure_ascii=False, indent=2)

# --- Export modèle IF pour déploiement ---
joblib.dump(if_model,         OUTPUT_DIR / 'isolation_forest_model.joblib')
joblib.dump(imputer,          OUTPUT_DIR / 'imputer.joblib')
joblib.dump(scaler,           OUTPUT_DIR / 'scaler.joblib')
joblib.dump(NUMERIC_FEATURES, OUTPUT_DIR / 'numeric_features.joblib')
joblib.dump({
    'threshold': threshold_if,
    'percentile': THRESHOLD_PERCENTILE,
    'contamination': contamination_if
}, OUTPUT_DIR / 'if_config.joblib')

# ═══════════════════════════════════════════════════════════════
#  RÉSUMÉ FINAL
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  TABLEAU FINAL DES MÉTRIQUES (EXÉCUTION RÉELLE)")
print("=" * 70)
summary = pd.DataFrame({
    'Isolation Forest': if_metrics,
    'One-Class SVM': ocsvm_metrics,
    'LSTM Autoencoder': lstm_metrics,
    'Random Forest': rf_metrics,
}).T[['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC', 'PR-AUC']]
print(summary.to_string())

print(f"\n  Fichiers sauvegardés dans : {OUTPUT_DIR}")
for f in sorted(OUTPUT_DIR.iterdir()):
    print(f"    {f.name:<40} {f.stat().st_size/1024:.1f} KB")

print("\n" + "=" * 70)
print("  AUDIT TERMINÉ AVEC SUCCÈS")
print("=" * 70)
