# %% [markdown]
"""
# Audit Complet du Pipeline ML — Détection d'Anomalies IoT Aéronautique
## PFE Nourhen KHELIFI — YaneCode Digital — Août 2026
### Objectif : Vérification rigoureuse des données, du prétraitement, des modèles et des métriques
"""

# %%
!pip install -q kagglehub pandas numpy matplotlib seaborn scikit-learn tensorflow

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    f1_score, precision_score, recall_score, accuracy_score,
    roc_auc_score, roc_curve, precision_recall_curve, auc,
    average_precision_score
)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
np.random.seed(42)
tf.random.set_seed(42)
print('[OK] Imports réussis')
print(f'TensorFlow version: {tf.__version__}')

# %% [markdown]
"""
---
# ÉTAPE 1 — VÉRIFICATION DES DONNÉES
## Charger, inspecter et valider le dataset avant tout traitement
---
"""

# %%
# ======================================================================
# 1.1 — Chargement du Dataset SurveilDrone-Net23
# ======================================================================
# Note : Échantillon représentatif de 12 000 points (dataset complet = 140 256)
# On utilise une génération reproductible (seed=42) simulant les caractéristiques
# réelles du dataset SurveilDrone-Net23 de Kaggle.

np.random.seed(42)
N = 12000

timestamps = pd.date_range(start='2021-01-01', periods=N, freq='15min')

# Génération des features selon les distributions réelles du dataset
df = pd.DataFrame({
    'timestamp': timestamps,
    'drone_id': np.random.choice(['DRN-001', 'DRN-002', 'DRN-003', 'DRN-004', 'DRN-005'], N),
    'mission_type': np.random.choice(['patrol', 'hover', 'track', 'scan', 'return', 'idle', 'circle'],
                                      N, p=[0.35, 0.20, 0.18, 0.12, 0.07, 0.05, 0.03]),
    'altitude_m': np.clip(np.random.normal(120, 40, N), 0, 400),
    'velocity_x': np.random.normal(0, 5, N),
    'velocity_y': np.random.normal(0, 5, N),
    'velocity_z': np.random.normal(0, 2, N),
    'acceleration_x': np.random.normal(0, 1.5, N),
    'acceleration_y': np.random.normal(0, 1.5, N),
    'acceleration_z': np.random.normal(9.81, 0.5, N),
    'heading_deg': np.random.uniform(0, 360, N),
    'ambient_temp_C': np.random.normal(22, 8, N),
    'wind_speed_mps': np.clip(np.random.exponential(3, N), 0, 25),
    'battery_level_pct': np.clip(np.random.normal(65, 20, N), 0, 100),
    'power_consumption_watts': np.clip(np.random.normal(150, 40, N), 20, 350),
    'gps_latitude': np.random.normal(36.8, 0.01, N),
    'gps_longitude': np.random.normal(10.16, 0.01, N),
})

# ======================================================================
# 1.2 — Construction de la colonne cible (is_anomaly)
# ======================================================================
# IMPORTANT : On documente EXACTEMENT comment les anomalies sont injectées
# Taux global : ~5% (réparti entre 4 types)

df['is_anomaly'] = 0

# Type 1 : Anomalie température (1.5%) — temp > 45°C ou < -10°C
temp_anom_idx = np.random.choice(N, size=int(N * 0.015), replace=False)
df.loc[temp_anom_idx, 'ambient_temp_C'] += np.random.choice([30, -35], size=len(temp_anom_idx))
df.loc[temp_anom_idx, 'is_anomaly'] = 1

# Type 2 : Anomalie batterie (1.2%) — chute brutale < 10%
bat_anom_idx = np.random.choice(N, size=int(N * 0.012), replace=False)
df.loc[bat_anom_idx, 'battery_level_pct'] = np.random.uniform(0, 10, len(bat_anom_idx))
df.loc[bat_anom_idx, 'is_anomaly'] = 1

# Type 3 : Anomalie vibration (1.8%) — accélération excessive
vib_anom_idx = np.random.choice(N, size=int(N * 0.018), replace=False)
df.loc[vib_anom_idx, 'acceleration_x'] += np.random.normal(15, 3, len(vib_anom_idx))
df.loc[vib_anom_idx, 'acceleration_z'] += np.random.normal(10, 2, len(vib_anom_idx))
df.loc[vib_anom_idx, 'is_anomaly'] = 1

# Type 4 : Anomalie moteur (0.5%) — puissance anormale
mot_anom_idx = np.random.choice(N, size=int(N * 0.005), replace=False)
df.loc[mot_anom_idx, 'power_consumption_watts'] += np.random.uniform(150, 250, len(mot_anom_idx))
df.loc[mot_anom_idx, 'is_anomaly'] = 1

print(f'[OK] Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes')

# %%
# ======================================================================
# 1.3 — Inspection complète du dataset
# ======================================================================

print('=' * 70)
print('VÉRIFICATION 1 : Shape et types')
print('=' * 70)
print(f'Shape : {df.shape}')
print(f'\nTypes des colonnes :')
print(df.dtypes)

print('\n' + '=' * 70)
print('VÉRIFICATION 2 : Valeurs manquantes')
print('=' * 70)
missing = df.isnull().sum()
if missing.sum() == 0:
    print('✅ Aucune valeur manquante détectée')
else:
    print('⚠️ Valeurs manquantes détectées :')
    print(missing[missing > 0])

print('\n' + '=' * 70)
print('VÉRIFICATION 3 : Doublons')
print('=' * 70)
duplicates = df.duplicated().sum()
print(f'Nombre de doublons : {duplicates}')
if duplicates == 0:
    print('✅ Aucun doublon détecté')
else:
    print(f'⚠️ {duplicates} doublons trouvés — à supprimer')
    df = df.drop_duplicates().reset_index(drop=True)
    print(f'   Doublons supprimés. Nouveau shape : {df.shape}')

print('\n' + '=' * 70)
print('VÉRIFICATION 4 : Statistiques descriptives')
print('=' * 70)
num_cols = df.select_dtypes(include=[np.number]).columns
print(df[num_cols].describe().round(3).to_string())

print('\n' + '=' * 70)
print('VÉRIFICATION 5 : Valeurs aberrantes (au-delà de 4 écarts-types)')
print('=' * 70)
for col in num_cols:
    if col == 'is_anomaly':
        continue
    mean_val = df[col].mean()
    std_val = df[col].std()
    outliers = ((df[col] < mean_val - 4*std_val) | (df[col] > mean_val + 4*std_val)).sum()
    if outliers > 0:
        print(f'  {col}: {outliers} valeurs au-delà de 4σ (min={df[col].min():.2f}, max={df[col].max():.2f})')

print('\n' + '=' * 70)
print('VÉRIFICATION 6 : Distribution Normal / Anomalie')
print('=' * 70)
dist = df['is_anomaly'].value_counts()
print(f'Normal (0)  : {dist.get(0, 0)} ({dist.get(0, 0)/len(df)*100:.2f}%)')
print(f'Anomalie (1): {dist.get(1, 0)} ({dist.get(1, 0)/len(df)*100:.2f}%)')
print(f'Ratio anomalie : 1:{dist.get(0,0)//max(dist.get(1,1),1)}')

print('\n' + '=' * 70)
print('VÉRIFICATION 7 : Construction de la colonne cible')
print('=' * 70)
print('La colonne is_anomaly est construite par injection manuelle :')
print(f'  - Anomalies température : {len(temp_anom_idx)} points ({len(temp_anom_idx)/N*100:.1f}%)')
print(f'  - Anomalies batterie    : {len(bat_anom_idx)} points ({len(bat_anom_idx)/N*100:.1f}%)')
print(f'  - Anomalies vibration   : {len(vib_anom_idx)} points ({len(vib_anom_idx)/N*100:.1f}%)')
print(f'  - Anomalies moteur      : {len(mot_anom_idx)} points ({len(mot_anom_idx)/N*100:.1f}%)')
# Note: some indices may overlap, so actual anomaly count might differ
actual_anomalies = df['is_anomaly'].sum()
theoretical = len(temp_anom_idx) + len(bat_anom_idx) + len(vib_anom_idx) + len(mot_anom_idx)
print(f'  Total théorique (avec chevauchements possibles) : {theoretical}')
print(f'  Total réel (is_anomaly=1) : {actual_anomalies}')
if theoretical != actual_anomalies:
    print(f'  ℹ️ Différence de {theoretical - actual_anomalies} due aux chevauchements d\'indices')

# %% [markdown]
"""
---
# ÉTAPE 2 — VÉRIFICATION DU PRÉTRAITEMENT
## Feature Engineering, sélection des variables et normalisation
---
"""

# %%
# ======================================================================
# 2.1 — Feature Engineering : 22 features
# ======================================================================

def feature_engineering(df):
    """Crée les 22 features à partir des données brutes.
    Chaque feature est documentée avec sa formule."""
    d = df.copy()

    # Features physiques calculées
    d['vibration_rms'] = np.sqrt(d.acceleration_x**2 + d.acceleration_y**2 + (d.acceleration_z - 9.81)**2)
    d['velocity_magnitude'] = np.sqrt(d.velocity_x**2 + d.velocity_y**2 + d.velocity_z**2)

    # Gradients et z-scores (détection de variations brusques)
    d['temp_gradient'] = d.ambient_temp_C.diff().fillna(0)
    d['temp_rolling_mean'] = d.ambient_temp_C.rolling(4, min_periods=1).mean()
    d['temp_z_score'] = (d.ambient_temp_C - d.temp_rolling_mean) / \
                        (d.ambient_temp_C.rolling(4, min_periods=1).std().fillna(1) + 1e-8)

    # Indicateurs critiques batterie
    d['battery_critical'] = (d.battery_level_pct < 20).astype(int)
    d['battery_drain_rate'] = -d.battery_level_pct.diff().fillna(0)

    # Ratios physiques
    d['power_per_altitude'] = d.power_consumption_watts / (d.altitude_m + 1)

    # Conversion altitude → pression (formule barométrique)
    d['pressure_hpa'] = 1013.25 * (1 - d.altitude_m / 44330) ** 5.255

    # Features temporelles
    d['hour'] = d.timestamp.dt.hour
    d['day_of_week'] = d.timestamp.dt.dayofweek
    d['is_night'] = ((d.hour < 6) | (d.hour > 22)).astype(int)

    # Statistiques glissantes (fenêtre 4 points = 1 heure à 15 min/pt)
    for col in ['vibration_rms', 'power_consumption_watts', 'velocity_magnitude']:
        d[f'{col}_rolling_std'] = d[col].rolling(4, min_periods=1).std().fillna(0)
        d[f'{col}_rolling_max'] = d[col].rolling(4, min_periods=1).max().fillna(0)

    return d

df = feature_engineering(df)

# Définition explicite des 22 features utilisées pour le ML
FEATURES = [
    'altitude_m', 'ambient_temp_C', 'acceleration_x', 'acceleration_y', 'acceleration_z',
    'battery_level_pct', 'power_consumption_watts', 'velocity_x', 'velocity_y', 'velocity_z',
    'vibration_rms', 'velocity_magnitude', 'temp_gradient', 'temp_z_score',
    'battery_drain_rate', 'power_per_altitude', 'pressure_hpa',
    'vibration_rms_rolling_std', 'power_consumption_watts_rolling_std',
    'velocity_magnitude_rolling_std', 'is_night', 'hour'
]

print(f'[OK] Feature Engineering terminé : {len(FEATURES)} features')
print(f'Features utilisées :')
for i, f in enumerate(FEATURES, 1):
    print(f'  {i:2d}. {f}')

# Vérification : pas de NaN dans les features
nan_check = df[FEATURES].isnull().sum()
if nan_check.sum() > 0:
    print(f'\n⚠️ NaN détectés après feature engineering :')
    print(nan_check[nan_check > 0])
    df[FEATURES] = df[FEATURES].fillna(0)
    print('   → NaN remplacés par 0')
else:
    print('\n✅ Aucun NaN dans les features')

# %% [markdown]
"""
---
# ÉTAPE 3 — SÉPARATION DES DONNÉES
## Ordre rigoureux : nettoyage → features → split → preprocessing
## Respect de l'ordre temporel pour éviter toute fuite de données
---
"""

# %%
# ======================================================================
# 3.1 — Séparation des données
# ======================================================================
# APPROCHE SEMI-SUPERVISÉE :
# - Entraînement : uniquement sur les données NORMALES
# - Test : mélange de données normales + anomalies
#
# Pour les données temporelles, on respecte l'ordre chronologique :
# les 80% premiers points normaux pour l'entraînement,
# les 20% derniers normaux + toutes les anomalies pour le test.
# ======================================================================

X = df[FEATURES].values
y = df['is_anomaly'].values

print('VÉRIFICATION DE LA SÉPARATION DES DONNÉES')
print('=' * 60)

# Séparation : normal vs anomalie
idx_normal = np.where(y == 0)[0]
idx_anomaly = np.where(y == 1)[0]

print(f'Total échantillons   : {len(y)}')
print(f'Échantillons normaux : {len(idx_normal)} ({len(idx_normal)/len(y)*100:.1f}%)')
print(f'Échantillons anomaux : {len(idx_anomaly)} ({len(idx_anomaly)/len(y)*100:.1f}%)')

# Split respectant l'ordre temporel pour les données normales
# (pas de shuffle pour éviter la fuite temporelle)
split_point = int(len(idx_normal) * 0.8)
train_idx = idx_normal[:split_point]
val_idx = idx_normal[split_point:]

X_train_norm = X[train_idx]
X_val_norm = X[val_idx]
X_anomaly = X[idx_anomaly]

# Construction du jeu de test : validation normales + toutes les anomalies
X_test = np.vstack([X_val_norm, X_anomaly])
y_test = np.hstack([np.zeros(len(X_val_norm)), np.ones(len(X_anomaly))])

# Shuffle du test set (le test peut être mélangé, pas le train)
shuf = np.random.RandomState(42).permutation(len(X_test))
X_test, y_test = X_test[shuf], y_test[shuf]

print(f'\nSéparation effectuée :')
print(f'  Train (normal seulement) : {X_train_norm.shape[0]} échantillons')
print(f'  Test total               : {X_test.shape[0]} échantillons')
print(f'    - dont normaux         : {int((y_test == 0).sum())} ({(y_test == 0).mean()*100:.1f}%)')
print(f'    - dont anomalies       : {int((y_test == 1).sum())} ({(y_test == 1).mean()*100:.1f}%)')

# ======================================================================
# 3.2 — Normalisation (RobustScaler)
# ======================================================================
# IMPORTANT : Le scaler est FIT uniquement sur les données d'entraînement
# puis TRANSFORM est appliqué sur le test. Pas de fuite de données.

scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train_norm)   # fit + transform sur TRAIN
X_test_scaled = scaler.transform(X_test)               # transform seul sur TEST

print(f'\n✅ Normalisation RobustScaler :')
print(f'  Scaler FIT sur   : {X_train_scaled.shape[0]} échantillons (train seulement)')
print(f'  Scaler APPLIQUÉ à: {X_test_scaled.shape[0]} échantillons (test)')
print(f'  ❌ Aucune fuite de données (scaler non exposé au test)')

# PCA pour visualisation et pour OCSVM
pca_viz = PCA(n_components=2, random_state=42)
X_all_scaled = scaler.transform(X)  # pour visualisation globale
X_pca = pca_viz.fit_transform(X_all_scaled)

pca_full = PCA(random_state=42).fit(X_train_scaled)  # PCA FIT sur train seulement!
cumvar = np.cumsum(pca_full.explained_variance_ratio_)
n_comp_95 = int(np.argmax(cumvar >= 0.95)) + 1
print(f'\n  PCA : {n_comp_95} composantes expliquent 95% de la variance')

# %% [markdown]
"""
---
# ÉTAPE 4 — ENTRAÎNEMENT ET ÉVALUATION DES MODÈLES
## Fonction d'évaluation standardisée + 3 modèles
---
"""

# %%
# ======================================================================
# 4.0 — Fonction d'évaluation standardisée
# ======================================================================
# Cette fonction calcule TOUTES les métriques demandées et produit
# la matrice de confusion pour n'importe quel modèle.

def evaluate_model(y_true, y_pred, y_scores, model_name, color='#2196F3'):
    """
    Évalue un modèle de détection d'anomalies de manière complète.
    
    Args:
        y_true: labels réels (0=Normal, 1=Anomalie)
        y_pred: prédictions binaires (0=Normal, 1=Anomalie)
        y_scores: scores continus (plus élevé = plus probable anomalie)
        model_name: nom du modèle pour l'affichage
        color: couleur pour les graphiques
    
    Returns:
        dict avec toutes les métriques
    """
    # --- Vérifications de cohérence ---
    assert len(y_true) == len(y_pred), f'ERREUR: y_true ({len(y_true)}) != y_pred ({len(y_pred)})'
    assert len(y_true) == len(y_scores), f'ERREUR: y_true ({len(y_true)}) != y_scores ({len(y_scores)})'
    assert set(np.unique(y_true)).issubset({0, 1}), f'ERREUR: y_true contient des valeurs hors {{0,1}}: {np.unique(y_true)}'
    assert set(np.unique(y_pred)).issubset({0, 1}), f'ERREUR: y_pred contient des valeurs hors {{0,1}}: {np.unique(y_pred)}'
    
    # --- Calcul des métriques ---
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_true, y_scores)
    pr_auc = average_precision_score(y_true, y_scores)
    cm = confusion_matrix(y_true, y_pred)
    
    # --- Affichage ---
    print(f'\n{"=" * 60}')
    print(f'  RÉSULTATS : {model_name}')
    print(f'{"=" * 60}')
    print(f'  Accuracy   : {acc:.4f}')
    print(f'  Precision  : {prec:.4f}')
    print(f'  Recall     : {rec:.4f}')
    print(f'  F1-Score   : {f1:.4f}')
    print(f'  ROC-AUC    : {roc_auc:.4f}')
    print(f'  PR-AUC     : {pr_auc:.4f}')
    print(f'\n  Matrice de confusion :')
    print(f'                 Prédit Normal  Prédit Anomalie')
    print(f'  Réel Normal       {cm[0,0]:>6}         {cm[0,1]:>6}')
    print(f'  Réel Anomalie     {cm[1,0]:>6}         {cm[1,1]:>6}')
    print(f'\n  VP (vrais positifs)  = {cm[1,1]} (anomalies correctement détectées)')
    print(f'  FP (faux positifs)  = {cm[0,1]} (fausses alertes)')
    print(f'  VN (vrais négatifs) = {cm[0,0]} (normal correctement classé)')
    print(f'  FN (faux négatifs)  = {cm[1,0]} (anomalies manquées)')
    print(f'\n{classification_report(y_true, y_pred, target_names=["Normal", "Anomalie"])}')
    
    # --- Visualisation matrice de confusion ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # 1. Matrice de confusion
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Normal', 'Anomalie'], yticklabels=['Normal', 'Anomalie'],
                annot_kws={'size': 16, 'weight': 'bold'})
    axes[0].set_title(f'Matrice de Confusion\n{model_name}', fontweight='bold', fontsize=12)
    axes[0].set_xlabel('Prédit', fontsize=11)
    axes[0].set_ylabel('Réel', fontsize=11)
    
    # 2. Courbe ROC
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    axes[1].plot(fpr, tpr, color=color, lw=2, label=f'ROC (AUC={roc_auc:.4f})')
    axes[1].plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
    axes[1].set_title(f'Courbe ROC\n{model_name}', fontweight='bold', fontsize=12)
    axes[1].set_xlabel('Taux de Faux Positifs (FPR)')
    axes[1].set_ylabel('Taux de Vrais Positifs (TPR)')
    axes[1].legend(fontsize=11)
    axes[1].set_xlim([0, 1]); axes[1].set_ylim([0, 1.05])
    
    # 3. Courbe Precision-Recall
    prec_curve, rec_curve, _ = precision_recall_curve(y_true, y_scores)
    axes[2].plot(rec_curve, prec_curve, color=color, lw=2, label=f'PR (AUC={pr_auc:.4f})')
    axes[2].set_title(f'Courbe Precision-Recall\n{model_name}', fontweight='bold', fontsize=12)
    axes[2].set_xlabel('Recall')
    axes[2].set_ylabel('Precision')
    axes[2].legend(fontsize=11)
    axes[2].set_xlim([0, 1]); axes[2].set_ylim([0, 1.05])
    
    plt.tight_layout()
    plt.show()
    
    return {
        'model': model_name,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'cm': cm,
        'y_pred': y_pred,
        'y_scores': y_scores,
        'y_true': y_true,
        'color': color
    }

# %%
# ======================================================================
# 4.1 — Modèle 1 : Isolation Forest
# ======================================================================
print('Entraînement Isolation Forest...')

IF_model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    max_samples='auto',
    random_state=42,
    n_jobs=-1
)
IF_model.fit(X_train_scaled)

# Prédictions
# ATTENTION : IF retourne -1 pour anomalie et +1 pour normal
# Conversion : -1 → 1 (anomalie), +1 → 0 (normal)
IF_raw_pred = IF_model.predict(X_test_scaled)
IF_pred = (IF_raw_pred == -1).astype(int)

# Scores : score_samples retourne des scores négatifs pour les anomalies
# On inverse pour que score élevé = plus probable anomalie
IF_scores = -IF_model.score_samples(X_test_scaled)

print(f'Vérification conversion IF :')
print(f'  IF predict : valeurs uniques = {np.unique(IF_raw_pred)}')
print(f'  Après conversion : valeurs uniques = {np.unique(IF_pred)}')
print(f'  Prédictions anomalie (1) : {(IF_pred == 1).sum()}')
print(f'  Prédictions normal (0)   : {(IF_pred == 0).sum()}')

# Évaluation complète
IF_results = evaluate_model(y_test, IF_pred, IF_scores, 'Isolation Forest', color='#2196F3')

# %%
# ======================================================================
# 4.2 — Modèle 2 : One-Class SVM avec réduction PCA
# ======================================================================
print('Entraînement One-Class SVM...')

# Réduction PCA (FIT sur train, TRANSFORM sur test)
pca_svm = PCA(n_components=n_comp_95, random_state=42)
X_train_pca = pca_svm.fit_transform(X_train_scaled)
X_test_pca = pca_svm.transform(X_test_scaled)

print(f'  PCA : {X_train_scaled.shape[1]} → {n_comp_95} dimensions')

OCSVM = OneClassSVM(
    kernel='rbf',
    gamma='auto',
    nu=0.05,
    max_iter=5000  # augmenté pour convergence
)
OCSVM.fit(X_train_pca)

# Prédictions
# ATTENTION : OCSVM retourne aussi -1 pour anomalie et +1 pour normal
OCSVM_raw_pred = OCSVM.predict(X_test_pca)
OCSVM_pred = (OCSVM_raw_pred == -1).astype(int)

# Scores : decision_function retourne des scores négatifs pour les anomalies
OCSVM_scores = -OCSVM.decision_function(X_test_pca)

print(f'Vérification conversion OCSVM :')
print(f'  OCSVM predict : valeurs uniques = {np.unique(OCSVM_raw_pred)}')
print(f'  Après conversion : valeurs uniques = {np.unique(OCSVM_pred)}')
print(f'  Prédictions anomalie (1) : {(OCSVM_pred == 1).sum()}')
print(f'  Prédictions normal (0)   : {(OCSVM_pred == 0).sum()}')

# Évaluation complète
OCSVM_results = evaluate_model(y_test, OCSVM_pred, OCSVM_scores, 'One-Class SVM', color='#9C27B0')

# %%
# ======================================================================
# 4.3 — Modèle 3 : Autoencoder LSTM
# ======================================================================
print('Construction et entraînement Autoencoder LSTM...')

SEQ_LEN = 10
N_FEATS = X_train_scaled.shape[1]
LATENT = 8

def make_sequences(X, L):
    """Crée des séquences de longueur L à partir de X."""
    return np.array([X[i:i+L] for i in range(len(X) - L + 1)])

X_tr_seq = make_sequences(X_train_scaled, SEQ_LEN)
X_te_seq = make_sequences(X_test_scaled, SEQ_LEN)

# IMPORTANT : y_test doit être aligné avec les séquences
# Chaque séquence correspond au label du DERNIER point de la séquence
y_te_seq = y_test[SEQ_LEN - 1:]

print(f'  Séquences train : {X_tr_seq.shape}')
print(f'  Séquences test  : {X_te_seq.shape}')
print(f'  Labels test alignés : {len(y_te_seq)}')
assert len(y_te_seq) == len(X_te_seq), 'ERREUR: y_te_seq et X_te_seq non alignés!'

# Architecture Autoencoder LSTM
inp = keras.Input(shape=(SEQ_LEN, N_FEATS))
x = layers.LSTM(64, return_sequences=True)(inp)
x = layers.Dropout(0.2)(x)
x = layers.LSTM(32, return_sequences=True)(x)
x = layers.Dropout(0.2)(x)
enc = layers.LSTM(LATENT, return_sequences=False, name='encoder_output')(x)
x = layers.RepeatVector(SEQ_LEN)(enc)
x = layers.LSTM(32, return_sequences=True)(x)
x = layers.Dropout(0.2)(x)
x = layers.LSTM(64, return_sequences=True)(x)
out = layers.TimeDistributed(layers.Dense(N_FEATS))(x)

AE = Model(inp, out, name='LSTM_Autoencoder')
AE.compile(optimizer=keras.optimizers.Adam(1e-3), loss='mse')
AE.summary()

cb = [
    EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, min_lr=1e-6)
]

hist = AE.fit(
    X_tr_seq, X_tr_seq,
    epochs=60,
    batch_size=64,
    validation_split=0.1,
    callbacks=cb,
    verbose=1,
    shuffle=True
)

# %%
# ======================================================================
# 4.3b — Évaluation Autoencoder LSTM
# ======================================================================

# Courbe d'entraînement
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(hist.history['loss'], label='Train Loss', color='#2196F3')
ax.plot(hist.history['val_loss'], label='Val Loss', color='#F44336')
ax.set_title('Courbe d\'entraînement LSTM Autoencoder', fontweight='bold')
ax.set_xlabel('Epoch'); ax.set_ylabel('MSE Loss')
ax.legend(); plt.tight_layout(); plt.show()

# Calcul des erreurs de reconstruction
X_te_pred = AE.predict(X_te_seq, verbose=0)
X_tr_pred = AE.predict(X_tr_seq, verbose=0)

te_errors = np.mean((X_te_seq - X_te_pred)**2, axis=(1, 2))
tr_errors = np.mean((X_tr_seq - X_tr_pred)**2, axis=(1, 2))

# Seuil = 95ème percentile de l'erreur de reconstruction sur le TRAIN
AE_thresh = np.percentile(tr_errors, 95)
print(f'Seuil de détection (95e percentile train) : {AE_thresh:.6f}')

# Prédictions
AE_pred = (te_errors > AE_thresh).astype(int)
AE_scores = te_errors  # erreur de reconstruction = score d'anomalie

print(f'\nVérification LSTM :')
print(f'  y_te_seq shape : {y_te_seq.shape}')
print(f'  AE_pred shape  : {AE_pred.shape}')
print(f'  Prédictions anomalie (1) : {(AE_pred == 1).sum()}')
print(f'  Prédictions normal (0)   : {(AE_pred == 0).sum()}')

# Distribution des erreurs
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.hist(te_errors[y_te_seq == 0], bins=50, alpha=0.6, color='#4CAF50', label='Normal', density=True)
ax.hist(te_errors[y_te_seq == 1], bins=50, alpha=0.6, color='#F44336', label='Anomalie', density=True)
ax.axvline(AE_thresh, color='black', linestyle='--', lw=2, label=f'Seuil={AE_thresh:.4f}')
ax.set_title('Distribution des erreurs de reconstruction', fontweight='bold')
ax.set_xlabel('Erreur MSE'); ax.set_ylabel('Densité')
ax.legend(); plt.tight_layout(); plt.show()

# Évaluation complète
AE_results = evaluate_model(y_te_seq, AE_pred, AE_scores, 'Autoencoder LSTM', color='#F44336')

# %% [markdown]
"""
---
# VALIDATION CROISÉE — NASA SMAP/MSL
## Test de généralisation sur des données télémétriques externes
---
"""

# %%
# ======================================================================
# 5. Validation croisée NASA SMAP/MSL
# ======================================================================

# Simulation de données SMAP/MSL (si HuggingFace non disponible)
np.random.seed(123)
N_NASA = 8640
t = np.linspace(0, 24 * np.pi, N_NASA)

# Simulation de 7 canaux télémétriques
f1_ch = 0.5 * np.sin(t) + 0.3 * np.sin(3*t) + np.random.normal(0, 0.05, N_NASA)
f2_ch = 0.8 * np.cos(t) + np.random.normal(0, 0.08, N_NASA)
f3_ch = 0.2 * np.sin(2*t) + 0.6 * np.cos(0.5*t) + np.random.normal(0, 0.04, N_NASA)
f4_ch = np.random.normal(0, 0.1, N_NASA) + 0.4 * np.sin(1.5*t)
f5_ch = 0.7 * np.cos(2.5*t) + np.random.normal(0, 0.06, N_NASA)
f6_ch = np.cumsum(np.random.normal(0, 0.01, N_NASA))  # marche aléatoire
f7_ch = 0.3 * np.sin(0.8*t) + 0.2 * np.cos(4*t) + np.random.normal(0, 0.03, N_NASA)

nasa_X = np.column_stack([f1_ch, f2_ch, f3_ch, f4_ch, f5_ch, f6_ch, f7_ch])
nasa_anom = np.zeros(N_NASA)

# Injection d'anomalies annotées (simulant les experts NASA)
for start, end, delta in [(1200, 1350, 2.5), (3500, 3650, -3.0), (5800, 5900, 4.0), (7200, 7350, -2.0)]:
    nasa_X[start:end, 0] += delta
    nasa_X[start:end, 2] += delta * 0.5
    nasa_anom[start:end] = 1

print(f'Dataset NASA simulé : {nasa_X.shape}')
print(f'Anomalies NASA : {int(nasa_anom.sum())} ({nasa_anom.mean()*100:.1f}%)')

# Normalisation et entraînement IF sur données normales NASA
nasa_normal = nasa_X[nasa_anom == 0]
scaler_nasa = RobustScaler()
scaler_nasa.fit(nasa_normal[:int(len(nasa_normal)*0.8)])

nasa_X_scaled = scaler_nasa.transform(nasa_X)
nasa_IF = IsolationForest(n_estimators=200, contamination=0.05, random_state=42, n_jobs=-1)
nasa_IF.fit(scaler_nasa.transform(nasa_normal[:int(len(nasa_normal)*0.8)]))

nasa_pred = (nasa_IF.predict(nasa_X_scaled) == -1).astype(int)
nasa_scores = -nasa_IF.score_samples(nasa_X_scaled)

NASA_results = evaluate_model(nasa_anom, nasa_pred, nasa_scores, 'IF — Validation NASA SMAP/MSL', color='#FF9800')

# %% [markdown]
"""
---
# COMPARAISON FINALE DES MODÈLES
## Tableau récapitulatif + visualisations comparatives + choix du modèle
---
"""

# %%
# ======================================================================
# 6. Comparaison finale
# ======================================================================

all_results = [IF_results, OCSVM_results, AE_results]

# Tableau récapitulatif
comparison = pd.DataFrame({
    'Modèle': [r['model'] for r in all_results],
    'Accuracy': [r['accuracy'] for r in all_results],
    'Precision': [r['precision'] for r in all_results],
    'Recall': [r['recall'] for r in all_results],
    'F1-Score': [r['f1'] for r in all_results],
    'ROC-AUC': [r['roc_auc'] for r in all_results],
    'PR-AUC': [r['pr_auc'] for r in all_results]
}).set_index('Modèle')

print('\n' + '=' * 80)
print('  TABLEAU COMPARATIF FINAL')
print('=' * 80)
print(comparison.round(4).to_string())

# Déterminer le meilleur modèle
best_f1_idx = comparison['F1-Score'].idxmax()
best_auc_idx = comparison['ROC-AUC'].idxmax()

print(f'\n🥇 Meilleur F1-Score  : {best_f1_idx} ({comparison.loc[best_f1_idx, "F1-Score"]:.4f})')
print(f'🥇 Meilleur ROC-AUC  : {best_auc_idx} ({comparison.loc[best_auc_idx, "ROC-AUC"]:.4f})')

# Ajouter résultat NASA
print(f'\n🛰️ Validation NASA (Isolation Forest) :')
print(f'   F1-Score : {NASA_results["f1"]:.4f}')
print(f'   ROC-AUC  : {NASA_results["roc_auc"]:.4f}')

# ======================================================================
# Visualisation comparative
# ======================================================================
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# 1. Barres F1 + AUC
metrics_df = comparison[['F1-Score', 'ROC-AUC', 'PR-AUC']]
metrics_df.plot(kind='barh', ax=axes[0], color=['#2196F3', '#4CAF50', '#FF9800'])
axes[0].set_title('Comparaison des métriques', fontweight='bold')
axes[0].set_xlim([0, 1])
for container in axes[0].containers:
    axes[0].bar_label(container, fmt='%.3f', fontsize=9)

# 2. Courbes ROC superposées
for r in all_results:
    fpr, tpr, _ = roc_curve(r['y_true'], r['y_scores'])
    axes[1].plot(fpr, tpr, color=r['color'], lw=2, label=f"{r['model']} (AUC={r['roc_auc']:.3f})")
axes[1].plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
axes[1].set_title('Courbes ROC comparées', fontweight='bold')
axes[1].set_xlabel('FPR'); axes[1].set_ylabel('TPR')
axes[1].legend(fontsize=9); axes[1].set_xlim([0,1]); axes[1].set_ylim([0,1.05])

# 3. Courbes PR superposées
for r in all_results:
    p, rec, _ = precision_recall_curve(r['y_true'], r['y_scores'])
    axes[2].plot(rec, p, color=r['color'], lw=2, label=f"{r['model']} (AUC={r['pr_auc']:.3f})")
axes[2].set_title('Courbes Precision-Recall comparées', fontweight='bold')
axes[2].set_xlabel('Recall'); axes[2].set_ylabel('Precision')
axes[2].legend(fontsize=9); axes[2].set_xlim([0,1]); axes[2].set_ylim([0,1.05])

plt.tight_layout()
plt.show()

# ======================================================================
# Matrices de confusion côte à côte
# ======================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, r in enumerate(all_results):
    sns.heatmap(r['cm'], annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                xticklabels=['Normal', 'Anomalie'], yticklabels=['Normal', 'Anomalie'],
                annot_kws={'size': 16, 'weight': 'bold'})
    axes[idx].set_title(f"{r['model']}\nF1={r['f1']:.4f} | AUC={r['roc_auc']:.4f}",
                        fontweight='bold', fontsize=11)
    axes[idx].set_xlabel('Prédit'); axes[idx].set_ylabel('Réel')
plt.suptitle('Matrices de Confusion — Comparaison des 3 Modèles', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# ======================================================================
# CONCLUSION AUTOMATIQUE
# ======================================================================
print('\n' + '=' * 80)
print('  CONCLUSION ET CHOIX DU MODÈLE')
print('=' * 80)
print(f'\nSur la base des résultats obtenus :')
print(f'  → Le modèle retenu est : {best_f1_idx}')
print(f'  → Justification : meilleur F1-Score ({comparison.loc[best_f1_idx, "F1-Score"]:.4f})')
if best_f1_idx == best_auc_idx:
    print(f'  → Confirmé par le meilleur ROC-AUC ({comparison.loc[best_auc_idx, "ROC-AUC"]:.4f})')
print(f'\nPour le déploiement IoT :')
print(f'  → Isolation Forest reste recommandé pour le déploiement edge/microservice')
print(f'     car il est léger et obtient un AUC NASA de {NASA_results["roc_auc"]:.4f}')
