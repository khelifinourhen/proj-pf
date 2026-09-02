$out = "C:\Users\hp\Desktop\Proj pf\notebooks\PFE_SurveilDrone_RealData_Models.ipynb"

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
# Étape 1 & 3 : Extraction des vraies données et Entraînement des Modèles
Ce notebook télécharge le **vrai dataset SurveilDrone-Net23**, sélectionne uniquement les colonnes correspondant à notre système embarqué (ESP32), et entraîne les 3 modèles d'IA pour les comparer.
"@

$cells += New-CodeCell @"
# Installation de kagglehub
!pip install -q kagglehub pandas numpy matplotlib seaborn scikit-learn tensorflow
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

# 1. Téléchargement des vraies données
print("Téléchargement du dataset SurveilDrone-Net23...")
path = kagglehub.dataset_download("datasetengineer/surveildrone-net23")
print("Chemin du dataset :", path)

# Trouver le fichier CSV principal
csv_files = glob.glob(os.path.join(path, "*.csv"))
if not csv_files:
    # Parfois il est dans un sous-dossier
    csv_files = glob.glob(os.path.join(path, "**", "*.csv"), recursive=True)

print("Fichiers trouvés :", csv_files)
df = pd.read_csv(csv_files[0])
print("\nDimensions originales :", df.shape)
"@

$cells += New-MdCell @"
## 2. Exploration et Filtrage des Colonnes
Nous voulons garder : Température, Pression/Altitude, Vitesse, Accélération/Vibration, Batterie, Puissance.
"@

$cells += New-CodeCell @"
print("--- Colonnes originales ---")
print(df.columns.tolist())
print("\n--- Types de données ---")
print(df.dtypes)
print("\n--- Valeurs manquantes ---")
print(df.isnull().sum())

# Filtrage robuste (on cherche des mots-clés dans les colonnes)
cols = df.columns.str.lower()
selected_cols = []

# Dictionnaire de recherche
keywords = {
    'temperature': ['temp'],
    'altitude_pressure': ['alt', 'press', 'baro'],
    'velocity': ['vel', 'speed'],
    'acceleration': ['acc', 'vib'],
    'battery': ['batt', 'volt', 'curr', 'pow']
}

for category, words in keywords.items():
    matched = [c for c, orig in zip(cols, df.columns) if any(w in c for w in words)]
    selected_cols.extend(matched)
    print(f"{category} -> colonnes trouvées : {matched}")

# Si on a une colonne cible (anomalie)
target_cols = [c for c in df.columns if 'anom' in c.lower() or 'label' in c.lower() or 'class' in c.lower() or 'status' in c.lower()]
print(f"Colonnes cibles trouvées : {target_cols}")

final_cols = list(set(selected_cols + target_cols))
df_clean = df[final_cols].copy()

# Nettoyage des valeurs manquantes (imputation ou suppression)
df_clean = df_clean.dropna()
print(f"\nDimensions finales après nettoyage : {df_clean.shape}")
df_clean.head()
"@

$cells += New-MdCell @"
## 3. Préparation pour le Machine Learning
Création des features comme l'amplitude de vibration, et séparation Train/Test.
"@

$cells += New-CodeCell @"
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

# S'il n'y a pas de colonne d'anomalie explicite, nous utiliserons la détection non supervisée pure,
# et nous simulerons des anomalies pour le test (comme dans Wokwi).
target_col = target_cols[0] if len(target_cols) > 0 else None

if target_col:
    # Transformation de la cible en binaire (0 = normal, 1 = anomalie)
    if df_clean[target_col].dtype == object:
        df_clean['is_anomaly'] = (df_clean[target_col] != df_clean[target_col].mode()[0]).astype(int)
    else:
        df_clean['is_anomaly'] = df_clean[target_col]
    
    # On drop la cible originale
    df_clean = df_clean.drop(columns=[target_col])
else:
    print("ATTENTION: Pas de colonne d'anomalie trouvée. Nous allons injecter des anomalies synthétiques pour évaluer les modèles.")
    df_clean['is_anomaly'] = 0
    # Injection aléatoire de pics (5% des données testées)
    idx_anom = df_clean.sample(frac=0.05).index
    df_clean.loc[idx_anom, 'is_anomaly'] = 1
    # On modifie une feature au hasard pour créer l'anomalie
    feat = df_clean.columns[0]
    df_clean.loc[idx_anom, feat] = df_clean[feat].max() * 2

X = df_clean.drop(columns=['is_anomaly']).values
y = df_clean['is_anomaly'].values

# Pour l'entraînement, on ne veut que des données normales (ou majoritairement normales)
X_normal = X[y == 0]
X_anom = X[y == 1]

# Split Train/Val sur les données normales
X_train, X_val = train_test_split(X_normal, test_size=0.2, random_state=42)

# Le Test set contient la validation normale + toutes les anomalies
X_test = np.vstack([X_val, X_anom])
y_test = np.hstack([np.zeros(len(X_val)), np.ones(len(X_anom))])

# Normalisation robuste aux outliers
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Train (Normal uniquement) : {X_train_scaled.shape}")
print(f"Test (Normal + Anomalies) : {X_test_scaled.shape} - Anomalies: {y_test.sum()}")
"@

$cells += New-MdCell @"
## 4. Entraînement et Comparaison des Modèles (Edge Computing Focus)
Nous évaluons le temps d'inférence (critique pour ESP32).
"@

$cells += New-CodeCell @"
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
import time
import tensorflow as tf
from tensorflow.keras import layers, Model

metrics = {}

# --- 1. ISOLATION FOREST ---
print("Entraînement Isolation Forest...")
start_time = time.time()
if_model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
if_model.fit(X_train_scaled)
if_train_time = time.time() - start_time

start_time = time.time()
if_preds = (if_model.predict(X_test_scaled) == -1).astype(int)
if_scores = -if_model.score_samples(X_test_scaled)
if_infer_time = (time.time() - start_time) / len(X_test_scaled) * 1000 # ms par sample

metrics['Isolation Forest'] = {
    'F1': f1_score(y_test, if_preds), 'AUC': roc_auc_score(y_test, if_scores),
    'Precision': precision_score(y_test, if_preds), 'Recall': recall_score(y_test, if_preds),
    'Train Time (s)': if_train_time, 'Inference Time (ms/sample)': if_infer_time,
    'Complexity': 'Low (Tree)'
}

# --- 2. ONE-CLASS SVM ---
print("Entraînement One-Class SVM...")
# OCSVM est très lent sur de gros datasets, on va l'entraîner sur un sous-échantillon si trop grand
X_train_svm = X_train_scaled[:15000] if len(X_train_scaled) > 15000 else X_train_scaled
start_time = time.time()
svm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
svm_model.fit(X_train_svm)
svm_train_time = time.time() - start_time

start_time = time.time()
svm_preds = (svm_model.predict(X_test_scaled) == -1).astype(int)
svm_scores = -svm_model.decision_function(X_test_scaled)
svm_infer_time = (time.time() - start_time) / len(X_test_scaled) * 1000

metrics['One-Class SVM'] = {
    'F1': f1_score(y_test, svm_preds), 'AUC': roc_auc_score(y_test, svm_scores),
    'Precision': precision_score(y_test, svm_preds), 'Recall': recall_score(y_test, svm_preds),
    'Train Time (s)': svm_train_time, 'Inference Time (ms/sample)': svm_infer_time,
    'Complexity': 'High (Kernel)'
}

# --- 3. AUTOENCODER LSTM ---
print("Entraînement Autoencoder LSTM...")
SEQ_LEN = 5
N_FEATS = X_train_scaled.shape[1]

def create_sequences(X, seq_length):
    return np.array([X[i:i+seq_length] for i in range(len(X)-seq_length)])

X_train_seq = create_sequences(X_train_scaled, SEQ_LEN)
X_test_seq = create_sequences(X_test_scaled, SEQ_LEN)
y_test_seq = y_test[SEQ_LEN:]

# Architecture allégée pour Edge
inputs = tf.keras.Input(shape=(SEQ_LEN, N_FEATS))
encoded = layers.LSTM(16, activation='relu')(inputs)
decoded = layers.RepeatVector(SEQ_LEN)(encoded)
decoded = layers.LSTM(16, activation='relu', return_sequences=True)(decoded)
outputs = layers.TimeDistributed(layers.Dense(N_FEATS))(decoded)
ae_model = Model(inputs, outputs)
ae_model.compile(optimizer='adam', loss='mse')

start_time = time.time()
ae_model.fit(X_train_seq, X_train_seq, epochs=10, batch_size=128, validation_split=0.1, verbose=0)
ae_train_time = time.time() - start_time

start_time = time.time()
ae_preds_raw = ae_model.predict(X_test_seq, verbose=0)
ae_infer_time = (time.time() - start_time) / len(X_test_seq) * 1000

# Calcul des erreurs de reconstruction
mse = np.mean(np.power(X_test_seq - ae_preds_raw, 2), axis=(1, 2))
threshold = np.percentile(np.mean(np.power(X_train_seq - ae_model.predict(X_train_seq, verbose=0), 2), axis=(1,2)), 95)
ae_preds = (mse > threshold).astype(int)

metrics['Autoencoder LSTM'] = {
    'F1': f1_score(y_test_seq, ae_preds), 'AUC': roc_auc_score(y_test_seq, mse),
    'Precision': precision_score(y_test_seq, ae_preds), 'Recall': recall_score(y_test_seq, ae_preds),
    'Train Time (s)': ae_train_time, 'Inference Time (ms/sample)': ae_infer_time,
    'Complexity': 'Very High (NN)'
}
"@

$cells += New-MdCell @"
## 5. Synthèse et Choix du Modèle pour l'Embarqué (ESP32)
"@

$cells += New-CodeCell @"
df_metrics = pd.DataFrame(metrics).T
print("=== RÉSULTATS DE COMPARAISON ===")
display(df_metrics.round(4))

# Visualisation des performances et du temps d'inférence
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
df_metrics[['F1', 'AUC', 'Precision', 'Recall']].plot(kind='bar', ax=ax1, colormap='viridis')
ax1.set_title("Performances de Détection")
ax1.set_ylim(0, 1.1)

df_metrics[['Inference Time (ms/sample)']].plot(kind='bar', ax=ax2, color='coral')
ax2.set_title("Temps d'inférence par échantillon (ms)")
ax2.set_ylabel("Millisecondes")
plt.tight_layout()
plt.show()

print("\nCONCLUSION RECOMMANDÉE :")
print("Pour une architecture Edge (ESP32) où la RAM et la latence sont critiques :")
print("- Si LSTM est trop lourd (temps inférence élevé, RAM ++), Isolation Forest est souvent le compromis idéal (faible empreinte mémoire, rapide).")
print("- La prochaine étape sera d'exporter le modèle choisi en C/C++ via micromlgen ou TensorFlow Lite for Microcontrollers.")
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
Write-Host "Notebook généré avec succès dans: $out"
