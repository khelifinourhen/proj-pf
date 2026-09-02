$out = "C:\Users\hp\Desktop\Proj pf\notebooks\anomaly_detection_iot_aeronautique.ipynb"

function New-MdCell($src) {
    return [PSCustomObject]@{
        cell_type = "markdown"
        metadata  = [PSCustomObject]@{}
        source    = $src -split "`n" | ForEach-Object { 
            if ($_ -match "\r$") { $_ = $_.Substring(0, $_.Length - 1) }
            "$_`n" 
        }
    }
}

function New-CodeCell($src) {
    return [PSCustomObject]@{
        cell_type       = "code"
        metadata        = [PSCustomObject]@{}
        source          = $src -split "`n" | ForEach-Object { 
            if ($_ -match "\r$") { $_ = $_.Substring(0, $_.Length - 1) }
            "$_`n" 
        }
        outputs         = @()
        execution_count = $null
    }
}

$cells = @()

$cells += New-MdCell @"
# Détection d'Anomalies IoT Aéronautique (Pipeline Complet ML/XAI)
## Projet de Fin d'Études — Pipeline ML Avancé pour architecture Edge (ESP32)

Ce notebook implémente la chaîne complète de traitement des données et d'apprentissage automatique, incluant :
- **Préparation stricte** : Gestion des NaN, doublons, valeurs aberrantes (IQR) et contraintes physiques.
- **Sélection de features** : Importance des variables et corrélations.
- **Entraînement non-supervisé** : Isolation Forest, One-Class SVM, LOF, Autoencoder LSTM (pas de SMOTE).
- **Optimisation** : Recherche d'hyperparamètres (GridSearch).
- **Évaluation** : PR-AUC, Matrice de confusion, Temps d'inférence.
- **Explicabilité (XAI)** : SHAP pour comprendre la cause de l'anomalie.
- **Risk Score** : Évaluation du risque de 0 à 100 pour Grafana.
"@

$cells += New-CodeCell @"
# Installation des dépendances (Google Colab)
!pip install -q kagglehub shap pandas numpy matplotlib seaborn scikit-learn tensorflow
"@

$cells += New-CodeCell @"
import kagglehub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import time
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.metrics import (f1_score, roc_auc_score, precision_score, recall_score, 
                             confusion_matrix, precision_recall_curve, auc, accuracy_score)
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.feature_selection import VarianceThreshold

import tensorflow as tf
from tensorflow.keras import layers, Model
import shap

plt.style.use('seaborn-v0_8-darkgrid')
"@

$cells += New-MdCell @"
## 1. Extraction et Préparation des Données (Vraies Données)
"@

$cells += New-CodeCell @"
print("Téléchargement du dataset SurveilDrone-Net23...")
path = kagglehub.dataset_download("datasetengineer/surveildrone-net23")
csv_files = glob.glob(os.path.join(path, "**", "*.csv"), recursive=True)
df = pd.read_csv(csv_files[0])
print(f"Dimensions originales : {df.shape}")

# Filtrage dynamique des colonnes
cols = df.columns.str.lower()
selected_cols = []
keywords = {
    'temperature': ['temp'],
    'altitude_pressure': ['alt', 'press', 'baro'],
    'velocity': ['vel', 'speed'],
    'acceleration': ['acc', 'vib'],
    'battery': ['batt', 'pow', 'curr', 'volt']
}
for cat, words in keywords.items():
    matched = [c for c, orig in zip(cols, df.columns) if any(w in c for w in words)]
    selected_cols.extend(matched)

target_cols = [c for c in df.columns if 'anom' in c.lower() or 'label' in c.lower() or 'class' in c.lower()]
final_cols = list(set(selected_cols + target_cols))

if 'timestamp' in df.columns:
    final_cols.append('timestamp')
elif 'time' in df.columns.str.lower():
    t_col = df.columns[df.columns.str.lower() == 'time'][0]
    final_cols.append(t_col)

df = df[final_cols].copy()
"@

$cells += New-MdCell @"
### A. Valeurs Manquantes, Doublons et Valeurs Incohérentes
"@

$cells += New-CodeCell @"
# A. Valeurs manquantes
print("--- Valeurs manquantes ---")
nan_counts = df.isnull().sum()
nan_pct = (nan_counts / len(df)) * 100
print(pd.DataFrame({'NaN Count': nan_counts, 'NaN %': nan_pct}))

# Imputation par interpolation temporelle ou médiane
df = df.interpolate(method='linear').fillna(df.median(numeric_only=True))

# B. Doublons
dups = df.duplicated().sum()
print(f"\n--- Doublons détectés : {dups} ---")
df = df.drop_duplicates()

# C. Valeurs Incohérentes (Contraintes physiques aéro)
print("\n--- Nettoyage des valeurs incohérentes ---")
for col in df.columns:
    col_l = col.lower()
    if 'batt' in col_l or 'pow' in col_l:
        df = df[(df[col] >= 0) & (df[col] <= 100)] if 'batt' in col_l else df[df[col] >= 0]
    elif 'temp' in col_l:
        df = df[(df[col] >= -50) & (df[col] <= 150)]  # Plage physique
    elif 'vel' in col_l or 'speed' in col_l:
        # Vitesse absolue >= 0 (si magnitude)
        pass

print(f"Dimensions après nettoyage physique : {df.shape}")
"@

$cells += New-MdCell @"
### D. Analyse des Outliers (IQR)
Nous utilisons l'IQR pour comprendre la distribution, mais nous ne supprimons pas les outliers, car en aéronautique, un outlier peut être la signature d'un comportement limite ou d'une anomalie.
"@

$cells += New-CodeCell @"
num_cols = df.select_dtypes(include=[np.number]).columns

outlier_summary = {}
for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    outlier_summary[col] = outliers_count

print("--- Nombre d'observations hors bornes IQR ---")
print(pd.Series(outlier_summary))
"@

$cells += New-MdCell @"
## 2. Feature Engineering & Feature Selection
"@

$cells += New-CodeCell @"
# Feature Engineering
d = df.copy()

# On identifie les colonnes pour créer des features complexes
acc_cols = [c for c in d.columns if 'acc' in c.lower() or 'vib' in c.lower()]
vel_cols = [c for c in d.columns if 'vel' in c.lower() or 'speed' in c.lower()]
temp_cols = [c for c in d.columns if 'temp' in c.lower()]
batt_cols = [c for c in d.columns if 'batt' in c.lower()]

if len(acc_cols) >= 3:
    d['vibration_rms'] = np.sqrt(d[acc_cols[0]]**2 + d[acc_cols[1]]**2 + d[acc_cols[2]]**2)
if len(vel_cols) >= 3:
    d['velocity_magnitude'] = np.sqrt(d[vel_cols[0]]**2 + d[vel_cols[1]]**2 + d[vel_cols[2]]**2)

if temp_cols:
    t_col = temp_cols[0]
    d['temp_gradient'] = d[t_col].diff().fillna(0)
    d['temp_rolling_mean'] = d[t_col].rolling(5, min_periods=1).mean()
    d['temp_z_score'] = (d[t_col] - d['temp_rolling_mean']) / (d[t_col].rolling(5, min_periods=1).std().fillna(1) + 1e-8)

if batt_cols:
    b_col = batt_cols[0]
    d['battery_critical'] = (d[b_col] < 20).astype(int)
    d['battery_drain_rate'] = -d[b_col].diff().fillna(0)

d = d.dropna()

# Séparation Cible / Features
target_col = target_cols[0] if target_cols else None
if target_col:
    if d[target_col].dtype == object:
        d['is_anomaly'] = (d[target_col] != d[target_col].mode()[0]).astype(int)
    else:
        d['is_anomaly'] = d[target_col]
    d = d.drop(columns=[target_col])
else:
    # Injection d'anomalies pour simulation si non présent
    d['is_anomaly'] = 0
    idx_anom = d.sample(frac=0.05, random_state=42).index
    d.loc[idx_anom, 'is_anomaly'] = 1
    if temp_cols:
        d.loc[idx_anom, temp_cols[0]] = d[temp_cols[0]].max() * 1.5

time_cols = [c for c in d.columns if 'time' in c.lower()]
X_df = d.drop(columns=['is_anomaly'] + time_cols)
y = d['is_anomaly'].values

# Feature Selection - Correlation & Random Forest Importance
corr = X_df.corr()

# RandomForest pour l'importance (utilisé juste pour l'analyse, pas pour le modèle final)
rf = RandomForestClassifier(n_estimators=50, random_state=42)
rf.fit(X_df, y)

feat_imp = pd.Series(rf.feature_importances_, index=X_df.columns).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
feat_imp.head(15).plot(kind='bar', color='teal')
plt.title("Importance des Variables (Random Forest)")
plt.ylabel("Score d'importance")
plt.tight_layout()
plt.show()

# Sélection des Top 15 features
TOP_FEATURES = feat_imp.head(15).index.tolist()
X_selected = X_df[TOP_FEATURES].values
print(f"Features sélectionnées : {TOP_FEATURES}")
"@

$cells += New-MdCell @"
## 3. Split Temporel et Normalisation
Pour l'IoT, une séparation temporelle empêche la fuite de données futures dans le passé.
"@

$cells += New-CodeCell @"
# Séparation temporelle (Chronologique) : 70% Train, 15% Val, 15% Test
n_samples = len(X_selected)
train_idx = int(n_samples * 0.70)
val_idx = int(n_samples * 0.85)

# Pour l'entraînement de nos modèles non-supervisés, le Train Set ne doit contenir QUE des données normales
X_train_full = X_selected[:train_idx]
y_train_full = y[:train_idx]

X_train_normal = X_train_full[y_train_full == 0]

X_val = X_selected[train_idx:val_idx]
y_val = y[train_idx:val_idx]

X_test = X_selected[val_idx:]
y_test = y[val_idx:]

scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train_normal)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print(f"Train Normal: {X_train_scaled.shape}")
print(f"Validation: {X_val_scaled.shape} (Anomalies: {y_val.sum()})")
print(f"Test: {X_test_scaled.shape} (Anomalies: {y_test.sum()})")
"@

$cells += New-MdCell @"
## 4. Optimisation et Entraînement des Modèles
Modèles : Isolation Forest, One-Class SVM, LOF, Autoencoder LSTM.
"@

$cells += New-CodeCell @"
metrics = {}

def evaluate_model(name, y_true, y_pred, y_scores, train_time, infer_time, complexity):
    cm = confusion_matrix(y_true, y_pred)
    pr, re, _ = precision_recall_curve(y_true, y_scores)
    pr_auc = auc(re, pr)
    
    metrics[name] = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, zero_division=0),
        'Recall': recall_score(y_true, y_pred, zero_division=0),
        'F1-Score': f1_score(y_true, y_pred, zero_division=0),
        'ROC-AUC': roc_auc_score(y_true, y_scores),
        'PR-AUC': pr_auc,
        'Train Time (s)': train_time,
        'Inference (ms/sample)': infer_time,
        'Complexity': complexity,
        'CM': cm
    }

# --- A. ISOLATION FOREST (Optimisé) ---
print("Optimisation Isolation Forest...")
best_if_f1 = 0
best_if = None

# Grid Search basique sur Validation
for n_est in [50, 100, 200]:
    for cont in [0.01, 0.05, 0.1]:
        m = IsolationForest(n_estimators=n_est, contamination=cont, random_state=42)
        m.fit(X_train_scaled)
        p = (m.predict(X_val_scaled) == -1).astype(int)
        f1 = f1_score(y_val, p, zero_division=0)
        if f1 > best_if_f1:
            best_if_f1 = f1
            best_if = m

start = time.time()
best_if.fit(X_train_scaled) # Re-fit final
train_time = time.time() - start

start = time.time()
preds = (best_if.predict(X_test_scaled) == -1).astype(int)
scores = -best_if.score_samples(X_test_scaled)
infer_time = (time.time() - start) / len(X_test_scaled) * 1000

evaluate_model('Isolation Forest', y_test, preds, scores, train_time, infer_time, 'Low (Tree)')

# --- B. ONE-CLASS SVM ---
print("Entraînement One-Class SVM...")
start = time.time()
svm = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
svm.fit(X_train_scaled[:10000]) # Subsample si trop gros
train_time = time.time() - start

start = time.time()
preds = (svm.predict(X_test_scaled) == -1).astype(int)
scores = -svm.decision_function(X_test_scaled)
infer_time = (time.time() - start) / len(X_test_scaled) * 1000

evaluate_model('One-Class SVM', y_test, preds, scores, train_time, infer_time, 'Medium (Kernel)')

# --- C. LOCAL OUTLIER FACTOR (LOF) ---
# Note: LOF en mode novelty=True pour prédiction sur données nouvelles
print("Entraînement LOF...")
start = time.time()
lof = LocalOutlierFactor(n_neighbors=20, novelty=True, contamination=0.05)
lof.fit(X_train_scaled)
train_time = time.time() - start

start = time.time()
preds = (lof.predict(X_test_scaled) == -1).astype(int)
scores = -lof.score_samples(X_test_scaled)
infer_time = (time.time() - start) / len(X_test_scaled) * 1000

evaluate_model('LOF', y_test, preds, scores, train_time, infer_time, 'Medium (KNN)')

# --- D. AUTOENCODER LSTM ---
print("Entraînement Autoencoder LSTM...")
SEQ_LEN = 5
N_FEATS = X_train_scaled.shape[1]

def create_seq(X, y, seq_len):
    Xs, ys = [], []
    for i in range(len(X) - seq_len):
        Xs.append(X[i:i+seq_len])
        ys.append(y[i+seq_len])
    return np.array(Xs), np.array(ys)

X_tr_seq, _ = create_seq(X_train_scaled, np.zeros(len(X_train_scaled)), SEQ_LEN)
X_val_seq, y_val_seq = create_seq(X_val_scaled, y_val, SEQ_LEN)
X_te_seq, y_te_seq = create_seq(X_test_scaled, y_test, SEQ_LEN)

inputs = tf.keras.Input(shape=(SEQ_LEN, N_FEATS))
x = layers.LSTM(16, activation='relu')(inputs)
x = layers.RepeatVector(SEQ_LEN)(x)
x = layers.LSTM(16, activation='relu', return_sequences=True)(x)
outputs = layers.TimeDistributed(layers.Dense(N_FEATS))(x)
ae = Model(inputs, outputs)
ae.compile(optimizer='adam', loss='mse')

start = time.time()
ae.fit(X_tr_seq, X_tr_seq, epochs=15, batch_size=64, validation_data=(X_val_seq, X_val_seq), verbose=0)
train_time = time.time() - start

start = time.time()
preds_raw = ae.predict(X_te_seq, verbose=0)
infer_time = (time.time() - start) / len(X_te_seq) * 1000

mse = np.mean(np.power(X_te_seq - preds_raw, 2), axis=(1, 2))
threshold = np.percentile(np.mean(np.power(X_val_seq - ae.predict(X_val_seq, verbose=0), 2), axis=(1,2)), 95)
preds = (mse > threshold).astype(int)

evaluate_model('Autoencoder LSTM', y_te_seq, preds, mse, train_time, infer_time, 'High (NN)')
"@

$cells += New-MdCell @"
## 5. Évaluation et Choix du Modèle
Focus sur PR-AUC (crucial pour les anomalies rares) et le Temps d'inférence.
"@

$cells += New-CodeCell @"
df_metrics = pd.DataFrame(metrics).T
display_df = df_metrics.drop(columns=['CM']).round(4)
print("=== PERFORMANCES ET RESSOURCES ===")
display(display_df)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Graphique 1 : Scores
display_df[['F1-Score', 'ROC-AUC', 'PR-AUC']].plot(kind='bar', ax=axes[0], colormap='viridis')
axes[0].set_title('Performances de Détection')
axes[0].set_ylim(0, 1.05)

# Graphique 2 : Inférence
display_df[['Inference (ms/sample)']].plot(kind='bar', ax=axes[1], color='coral')
axes[1].set_title('Temps d\'inférence (ms) - Critique Edge')

# Graphique 3 : Matrice Confusion (Isolation Forest)
cm_if = metrics['Isolation Forest']['CM']
sns.heatmap(cm_if, annot=True, fmt='d', cmap='Blues', ax=axes[2],
            xticklabels=['Prédit Normal', 'Prédit Anomalie'],
            yticklabels=['Réel Normal', 'Réel Anomalie'])
axes[2].set_title('Matrice Confusion - Isolation Forest')

plt.tight_layout()
plt.show()
"@

$cells += New-MdCell @"
## 6. eXplainable AI (XAI) avec SHAP
Pourquoi le système a-t-il déclaré cette mesure comme anormale ?
Nous utilisons SHAP sur Isolation Forest.
"@

$cells += New-CodeCell @"
print("Calcul des valeurs SHAP pour Isolation Forest...")

# SHAP TreeExplainer est optimisé pour Isolation Forest
explainer = shap.TreeExplainer(best_if)

# On sélectionne quelques anomalies détectées pour les analyser
idx_anomalies_pred = np.where(metrics['Isolation Forest']['CM'] != 0)[0] # Juste pour bypass array logic in raw code
preds_if = (best_if.predict(X_test_scaled) == -1).astype(int)
anom_indices = np.where((preds_if == 1) & (y_test == 1))[0] # Vrais positifs

if len(anom_indices) > 0:
    sample_idx = anom_indices[0]
    sample = X_test_scaled[sample_idx:sample_idx+1]
    
    shap_values = explainer.shap_values(sample)
    
    # SHAP force plot / waterfall plot logic textuellement
    print(f"\n--- Analyse de l'anomalie Vrai Positif (Index {sample_idx}) ---")
    
    feature_contributions = pd.Series(shap_values[0], index=TOP_FEATURES)
    print("Contributions des features à l'anomalie (Valeurs SHAP) :")
    print(feature_contributions.sort_values(ascending=False).head(5))
    
    plt.figure(figsize=(8, 4))
    feature_contributions.sort_values(ascending=True).tail(8).plot(kind='barh', color='crimson')
    plt.title(f"Top Features expliquant l'anomalie n°{sample_idx}")
    plt.xlabel("Valeur SHAP (Impact sur le score)")
    plt.tight_layout()
    plt.show()
else:
    print("Aucun vrai positif détecté pour SHAP dans ce sous-échantillon.")
"@

$cells += New-MdCell @"
## 7. Calcul du Risk Score (0 - 100)
Génération d'un score dynamique combinant le modèle IA et les valeurs brutes critiques pour le dashboard Grafana.
"@

$cells += New-CodeCell @"
def calculate_risk_score(anomaly_score, temp_val, batt_val, max_temp=85, min_batt=15):
    """
    Combine l'output du modèle IA avec des seuils métiers pour générer un Risk Score de 0 à 100.
    - anomaly_score : score de base normalisé entre 0 et 1.
    - temp_val : Température actuelle
    - batt_val : Batterie restante
    """
    # 1. Base issue de l'IA (poids 60%)
    risk_ia = np.clip(anomaly_score * 100, 0, 100) * 0.6
    
    # 2. Règle Métier : Température (poids 20%)
    risk_temp = 0
    if temp_val > max_temp:
        risk_temp = 20
    elif temp_val > max_temp - 10:
        risk_temp = 10
        
    # 3. Règle Métier : Batterie critique (poids 20%)
    risk_batt = 0
    if batt_val < min_batt:
        risk_batt = 20
    elif batt_val < min_batt + 10:
        risk_batt = 10
        
    total_risk = min(100, risk_ia + risk_temp + risk_batt)
    
    # Classification
    if total_risk < 30:
        status = "🟢 Normal"
    elif total_risk < 60:
        status = "🟡 Attention"
    elif total_risk < 80:
        status = "🟠 Risque"
    else:
        status = "🔴 Critique"
        
    return total_risk, status

# Exemple sur l'échantillon testé par SHAP
if len(anom_indices) > 0:
    # On récupère le score d'anomalie normalisé (0 à 1)
    base_scores = -best_if.score_samples(X_test_scaled)
    min_s, max_s = base_scores.min(), base_scores.max()
    norm_scores = (base_scores - min_s) / (max_s - min_s)
    
    raw_temp = X_test[sample_idx, TOP_FEATURES.index(temp_cols[0])] if temp_cols else 25
    raw_batt = X_test[sample_idx, TOP_FEATURES.index(batt_cols[0])] if batt_cols else 50
    
    score, status = calculate_risk_score(norm_scores[sample_idx], raw_temp, raw_batt)
    print(f"\nExemple d'évaluation Risk Score sur une anomalie :")
    print(f"Risk Score : {score:.1f}/100 => État : {status}")
    print(f"(Température: {raw_temp:.1f}C, Batterie: {raw_batt:.1f}%, IA Score Normalisé: {norm_scores[sample_idx]:.2f})")
"@

$notebook = [PSCustomObject]@{
    nbformat = 4
    nbformat_minor = 5
    metadata = [PSCustomObject]@{
        kernelspec = [PSCustomObject]@{
            display_name = "Python 3"
            language = "python"
            name = "python3"
        }
    }
    cells = $cells
}

$json = $notebook | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($out, $json, [System.Text.Encoding]::UTF8)
Write-Host "Notebook final généré avec succès dans: $out"
