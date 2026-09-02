# GUIDE COMPLET — LANCEMENT & DÉPLOIEMENT
## Projet PFE : Détection d'Anomalies IoT Aéronautique
**Nourhen KHELIFI | 2025/2026**

---

> [!IMPORTANT]
> Lire ce guide dans l'ordre exact. Chaque étape dépend de la précédente.
> **Durée totale estimée : 20–30 minutes pour tout lancer la première fois.**

---

## ARCHITECTURE DE LA CHAÎNE COMPLÈTE

```
┌──────────────────────────────────────────────────────┐
│                  GOOGLE COLAB                        │
│  Dataset → Preprocessing → Training → Validation    │
│              model_pipeline.joblib                  │
└────────────────────┬─────────────────────────────────┘
                     │ joblib
                     ▼
┌──────────────────────────────────────────────────────┐
│                    GITHUB                            │
│  iot-anomaly-detection/ (code + modèle + docs)      │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│              API PYTHON (Flask)                      │
│  localhost:5000/predict                             │
│  Isolation Forest + Preprocessing Pipeline          │
└───────────────┬─────────────────────────────────────┘
                │ HTTP POST ↑↓ JSON
┌───────────────┴─────────────────────────────────────┐
│                  NODE-RED                            │
│  MQTT → Validation → Préparation → ML → Fusion     │
└──────────┬──────────────────────────────────────────┘
           │ MQTT                        │ Write
┌──────────┴──────────┐       ┌──────────▼──────────┐
│  ESP32 / WOKWI      │       │      INFLUXDB        │
│  HiveMQ MQTT Broker │       │  sensors_ml measure  │
└─────────────────────┘       └──────────┬──────────┘
                                          │ Query
                               ┌──────────▼──────────┐
                               │       GRAFANA        │
                               │  Dashboard + Alertes │
                               └─────────────────────┘
```

---

## FICHIERS DU PROJET

| Fichier | Taille | Rôle |
|---|---|---|
| `model/model_pipeline.joblib` | 2.7 MB | Pipeline ML complet (imputer+scaler+IF) |
| `model/if_config.joblib` | 0.1 KB | Seuil de détection (P95 = 0.5234) |
| `model/metadata.json` | 1.6 KB | Métadonnées, features, métriques |
| `api/app_flask.py` | 8.0 KB | **API Flask principale** |
| `api/app.py` | 12.8 KB | API FastAPI (alternative) |
| `api/requirements.txt` | 0.1 KB | Dépendances Python |
| `node-red/flow.json` | 8.7 KB | Flux Node-RED complet |
| `grafana/dashboard.json` | 5.1 KB | Dashboard 9 panneaux |
| `tests/test_scenarios.py` | 3.5 KB | Test 3 scénarios |
| `tests/test_api.py` | 8.6 KB | Suite pytest complète |
| `train_and_save_pipeline.py` | 5.8 KB | Script d'entraînement |
| `Dockerfile` | 0.3 KB | Conteneurisation Docker |
| `README.md` | 5.6 KB | Documentation GitHub |

---

## ÉTAPE 1 — LANCER L'API FLASK (ML Service)

> **C'est la première chose à démarrer.** Node-RED en dépend.

### 1.1 Ouvrir un terminal PowerShell

```powershell
# Dans le dossier du projet
cd "c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection"
```

### 1.2 Lancer le serveur Flask

```powershell
F:\ml_env\venv\Scripts\python.exe api\app_flask.py
```

**Sortie attendue :**
```
2026-08-27 18:30:00 | INFO | Modele charge : IsolationForest v2.0
2026-08-27 18:30:00 | INFO | Features      : 24
2026-08-27 18:30:00 | INFO | Seuil         : 0.523398 (P95)
 * Running on http://0.0.0.0:5000
```

> [!NOTE]
> L'API doit rester **ouverte dans ce terminal** pendant toute la démonstration.
> Ouvrir un **deuxième terminal** pour les tests.

---

## ÉTAPE 2 — VÉRIFIER QUE L'API FONCTIONNE

### 2.1 Test /health (dans un 2e terminal)

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET | Select-Object -ExpandProperty Content
```

**Réponse attendue :**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model": "IsolationForest",
  "version": "2.0",
  "uptime_seconds": 5.1,
  "predictions_made": 0,
  "anomalies_found": 0
}
```

### 2.2 Test /predict — Scénario NORMAL

```powershell
$body = '{"temperature_c":24.5,"pressure_hpa":1013.0,"humidity_pct":52.0,"vibration_norm_ms2":0.12,"voltage_v":3.3,"rpm":1450.0}'
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Method POST -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

**Réponse attendue :**
```json
{
  "anomaly": 0,
  "anomaly_score": 0.506,
  "status": "NORMAL",
  "model": "IsolationForest",
  "threshold": 0.5234,
  "timestamp": "2026-08-27T17:30:00Z",
  "message": "Comportement normal"
}
```

### 2.3 Test /predict — Scénario ANOMALIE

```powershell
$body = '{"temperature_c":142.0,"pressure_hpa":650.0,"vibration_norm_ms2":15.3,"voltage_v":2.4,"current_a":4.8,"rpm":5500.0,"motor_current_temp_c":148.0}'
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Method POST -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

**Réponse attendue :**
```json
{
  "anomaly": 1,
  "anomaly_score": 0.5645,
  "status": "ANOMALY",
  "message": "Anomalie detectee (score=0.565)"
}
```

### 2.4 Test rapide des 3 scénarios d'un coup

```powershell
F:\ml_env\venv\Scripts\python.exe tests\test_scenarios.py
```

**Sortie attendue :**
```
SCENARIO 1 NOMINAL  : score=0.5061 | NORMAL   ✅
SCENARIO 2 LIMITE   : score=0.4714 | NORMAL   ✅
SCENARIO 3 ANOMALIE : score=0.5645 | ANOMALY  ✅
```

---

## ÉTAPE 3 — CONFIGURER NODE-RED

### 3.1 Lancer Node-RED

```powershell
# Si Node-RED est installé globalement
node-red
```
Ou depuis le menu Démarrer → Node-RED.

Ouvrir : **http://localhost:1880**

### 3.2 Importer le flux

1. Cliquer sur le menu **≡** (hamburger, haut à droite)
2. Cliquer sur **Import**
3. Cliquer sur **select a file to import**
4. Sélectionner : `c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection\node-red\flow.json`
5. Cliquer sur **Import**
6. Cliquer sur **Deploy** (bouton rouge en haut à droite)

### 3.3 Configurer le broker MQTT (HiveMQ)

Double-cliquer sur le nœud **"ESP32 MQTT IN (HiveMQ)"** :
- **Server** : `broker.hivemq.com`
- **Port** : `1883`
- **Topic** : `aeronautique/esp32/sensors`

### 3.4 Configurer InfluxDB

Double-cliquer sur le nœud **"InfluxDB -> sensors_ml"** :
- **Host** : `localhost`
- **Port** : `8086`
- **Database** : `aeronautique_iot`
- **Measurement** : `sensors_ml`

### 3.5 Vérifier que l'URL ML est correcte

Double-cliquer sur le nœud **"HTTP -> ML API /predict"** :
- **URL** : `http://localhost:5000/predict`
- **Method** : `POST`
- **Return** : `a parsed JSON object`

### 3.6 Tester depuis Node-RED (sans ESP32)

Les nœuds **Inject** sont déjà configurés avec les 3 scénarios :
- Cliquer sur le bouton gris à gauche de **"Test: Scenario NORMAL"** → vérifier que le résultat arrive dans InfluxDB
- Cliquer sur **"Test: Scenario ANOMALIE"** → vérifier qu'une alerte apparaît dans le panneau Debug

---

## ÉTAPE 4 — CONFIGURER INFLUXDB

### 4.1 Vérifier qu'InfluxDB tourne

Ouvrir : **http://localhost:8086**

### 4.2 Créer la base de données (si pas déjà fait)

Dans InfluxDB UI ou via le terminal :

```powershell
# Via l'API InfluxDB
Invoke-WebRequest -Uri "http://localhost:8086/query" -Method POST -Body "q=CREATE DATABASE aeronautique_iot" | Select-Object StatusCode
```

### 4.3 Vérifier les données après injection Node-RED

```powershell
# Lire les dernières mesures
$q = [System.Uri]::EscapeDataString("SELECT * FROM sensors_ml ORDER BY time DESC LIMIT 5")
Invoke-WebRequest -Uri "http://localhost:8086/query?db=aeronautique_iot&q=$q" | Select-Object -ExpandProperty Content
```

**Champs attendus dans InfluxDB :**
```
temperature_c, pressure_hpa, humidity_pct, vibration_norm_ms2,
voltage_v, current_a, power_w, rpm,
ml_anomaly, ml_anomaly_score, ml_status, ml_threshold, ml_model
```

---

## ÉTAPE 5 — CONFIGURER GRAFANA

### 5.1 Ouvrir Grafana

**http://localhost:3000**  
Login : `admin` / `admin` (ou votre mot de passe)

### 5.2 Ajouter la datasource InfluxDB

1. Menu gauche → **Connections** → **Data sources**
2. Cliquer **+ Add new data source**
3. Choisir **InfluxDB**
4. Configuration :
   - **URL** : `http://localhost:8086`
   - **Database** : `aeronautique_iot`
   - **User** : (laisser vide)
5. Cliquer **Save & test** → doit afficher ✅ "datasource is working"

### 5.3 Importer le dashboard

1. Menu gauche → **Dashboards** → **Import**
2. Cliquer **Upload dashboard JSON file**
3. Sélectionner : `c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection\grafana\dashboard.json`
4. Choisir la datasource **InfluxDB** dans le sélecteur
5. Cliquer **Import**

### 5.4 Panneaux disponibles dans le dashboard

| Panneau | Type | Description |
|---|---|---|
| 1 | Stat | Statut NORMAL / ANOMALY (temps réel) |
| 2 | Time series | Score d'anomalie ML (évolution) |
| 3 | Stat | Nombre d'anomalies détectées |
| 4 | Time series | Température (°C) |
| 5 | Time series | Pression (hPa) |
| 6 | Time series | Vibrations (m/s²) |
| 7 | Time series | Voltage (V) |
| 8 | Table | Dernières anomalies détectées (20 dernières) |
| 9 | Gauge | RPM Moteur |

---

## ÉTAPE 6 — CONNECTER L'ESP32 / WOKWI

### 6.1 Topic MQTT attendu

L'ESP32 (ou Wokwi) doit publier sur :
```
Topic : aeronautique/esp32/sensors
```

### 6.2 Format JSON attendu

```json
{
  "temperature_c": 25.4,
  "pressure_hpa": 1012.5,
  "humidity_pct": 55.0,
  "altitude_m": 3000.0,
  "airspeed_kts": 250.0,
  "vibration_norm_ms2": 0.15,
  "voltage_v": 3.3,
  "current_a": 0.85,
  "power_w": 2.8,
  "rpm": 1450.0,
  "operating_hours": 1200.0,
  "load_pct": 55.0,
  "motor_current_temp_c": 45.0,
  "wifi_rssi_dbm": -65.0,
  "packet_latency_ms": 12.0
}
```

> [!IMPORTANT]
> **Variables interdites — NE PAS envoyer :**
> - `fault_injection_level_pct` (variable de simulation, non disponible en production)
> - `failure_type`, `failure_event`, `anomaly_reference` (labels)
> 
> Node-RED les ignore automatiquement grâce au nœud "Préparation Input ML".

### 6.3 Simulation manuelle depuis PowerShell (sans ESP32)

```powershell
# Installer un client MQTT
# mqtt.js ou mosquitto_pub

# Exemple avec mosquitto_pub (si installé)
mosquitto_pub -h broker.hivemq.com -p 1883 -t "aeronautique/esp32/sensors" -m '{"temperature_c":24.5,"pressure_hpa":1013.0,"vibration_norm_ms2":0.12,"voltage_v":3.3,"rpm":1450.0}'
```

---

## ÉTAPE 7 — TESTS DES 3 SCÉNARIOS COMPLETS

### Scénario 1 — VOL NOMINAL

**Objectif :** Vérifier que le système classe correctement un vol normal.

**Via les nœuds Inject Node-RED :** Cliquer sur **"Test: Scenario NORMAL"**

**Via PowerShell :**
```powershell
$body = '{"temperature_c":24.5,"pressure_hpa":1013.0,"humidity_pct":52.0,"altitude_m":3000.0,"airspeed_kts":250.0,"vibration_norm_ms2":0.12,"voltage_v":3.3,"current_a":0.85,"power_w":2.8,"rpm":1450.0,"operating_hours":1200.0,"load_pct":55.0,"motor_current_temp_c":45.0,"wifi_rssi_dbm":-65.0,"packet_latency_ms":12.0}'
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Method POST -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

**Résultat attendu :** `"status": "NORMAL"` | Score ≈ 0.506

**Vérification Grafana :** Panneau 1 → vert **NORMAL** | Panneau 2 → score < 0.523

---

### Scénario 2 — PARAMÈTRES LIMITES

**Objectif :** Vérifier le comportement aux limites opérationnelles.

**Via Node-RED :** Cliquer sur **"Test: Scenario LIMITE"**

**Via PowerShell :**
```powershell
$body = '{"temperature_c":68.0,"pressure_hpa":980.0,"humidity_pct":88.0,"altitude_m":9500.0,"airspeed_kts":420.0,"vibration_norm_ms2":1.8,"voltage_v":3.1,"current_a":1.9,"power_w":5.9,"rpm":2800.0,"operating_hours":4800.0,"load_pct":89.0,"motor_current_temp_c":88.0,"wifi_rssi_dbm":-85.0,"packet_latency_ms":95.0}'
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Method POST -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

**Résultat attendu :** `"status": "NORMAL"` | Score ≈ 0.471 (proche du seuil, surveillance recommandée)

---

### Scénario 3 — ANOMALIE CRITIQUE

**Objectif :** Vérifier que le système détecte une surchauffe + vibrations critiques.

**Via Node-RED :** Cliquer sur **"Test: Scenario ANOMALIE"**

**Via PowerShell :**
```powershell
$body = '{"temperature_c":142.0,"pressure_hpa":650.0,"humidity_pct":98.0,"altitude_m":12000.0,"airspeed_kts":580.0,"vibration_norm_ms2":15.3,"voltage_v":2.4,"current_a":4.8,"power_w":11.5,"rpm":5500.0,"operating_hours":8900.0,"load_pct":97.0,"motor_current_temp_c":148.0,"wifi_rssi_dbm":-95.0,"packet_latency_ms":380.0}'
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Method POST -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

**Résultat attendu :** `"status": "ANOMALY"` | Score ≈ 0.565 > seuil 0.523

**Vérification Grafana :** Panneau 1 → rouge **ANOMALY** | Panneau 3 → compteur anomalies +1

---

## ÉTAPE 8 — POUSSER SUR GITHUB

### 8.1 Créer le dépôt sur GitHub

1. Aller sur **https://github.com/new**
2. Nom du dépôt : `iot-anomaly-detection`
3. Description : `Solution IoT embarquée pour monitoring aéronautique et détection d'anomalies ML - PFE 2025/2026`
4. Visibilité : **Public** (ou Private selon votre choix)
5. **NE PAS** cocher "Initialize this repository"
6. Cliquer **Create repository**

### 8.2 Connecter et pousser le dépôt local

```powershell
cd "c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection"

# Remplacer VOTRE_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE_USERNAME/iot-anomaly-detection.git

# Pousser
git push -u origin main
```

> [!NOTE]
> GitHub va vous demander votre **username** et un **Personal Access Token** (PAT).  
> Pour créer un PAT : GitHub → Settings → Developer Settings → Personal Access Tokens → Generate new token (classic) → cocher `repo`.

### 8.3 Vérifier le push

Aller sur `https://github.com/VOTRE_USERNAME/iot-anomaly-detection`

Vous devez voir :
```
iot-anomaly-detection/
├── api/           (app_flask.py, app.py, requirements.txt)
├── model/         (model_pipeline.joblib, metadata.json, if_config.joblib)
├── node-red/      (flow.json)
├── grafana/       (dashboard.json)
├── tests/         (test_api.py, test_scenarios.py)
├── Dockerfile
├── README.md
└── train_and_save_pipeline.py
```

> [!TIP]
> Si `model_pipeline.joblib` (2.7 MB) est rejeté par GitHub (limite 100 MB), il est bien en dessous — aucun problème.
> Pour les gros modèles futurs, utiliser **Git LFS** : `git lfs track "*.joblib"`

### 8.4 Ajouter un tag de version

```powershell
git tag -a v1.0.0 -m "Version finale PFE 2025/2026 - Pipeline IF + Flask API"
git push origin v1.0.0
```

---

## ÉTAPE 9 — DÉPLOIEMENT DOCKER (optionnel pour soutenance)

```powershell
cd "c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection"

# Construire l'image
docker build -t anomaly-api:latest .

# Lancer le conteneur
docker run -p 5000:5000 --name ml-service anomaly-api:latest

# Vérifier
Invoke-WebRequest http://localhost:5000/health | Select-Object -ExpandProperty Content

# Arrêter
docker stop ml-service
```

---

## RÉSUMÉ — ORDRE DE LANCEMENT POUR LA DÉMO

```
┌─────────────────────────────────────────────────────────────┐
│ ORDRE DE LANCEMENT (respecter cet ordre)                   │
│                                                             │
│  ① InfluxDB     → doit tourner en arrière-plan             │
│  ② API Flask    → terminal 1 : python api\app_flask.py     │
│  ③ Node-RED     → déjà configuré → Deploy                  │
│  ④ Grafana      → ouvrir http://localhost:3000             │
│  ⑤ ESP32/Wokwi → publie sur MQTT → tout se déclenche      │
│                                                             │
│  Tester sans ESP32 : boutons Inject dans Node-RED          │
└─────────────────────────────────────────────────────────────┘
```

### Commande unique de lancement API

```powershell
F:\ml_env\venv\Scripts\python.exe "c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection\api\app_flask.py"
```

---

## MÉTRIQUES DU MODÈLE (résultats définitifs)

| Modèle | ROC-AUC | F1-score | Precision | Recall | Recommandation |
|---|---:|---:|---:|---:|---|
| Isolation Forest | 0.6921 | 0.2511 | 0.2915 | 0.2205 | Déploiement non supervisé |
| One-Class SVM | 0.6310 | 0.3097 | 0.3923 | 0.2559 | Non recommandé |
| LSTM Autoencoder | 0.6835 | 0.2314 | 0.3111 | 0.1842 | Trop complexe IoT Edge |
| **Random Forest** | **0.9728** | **0.7774** | **0.9387** | 0.6634 | Supervisé — production |

**Modèle déployé :** Isolation Forest (non supervisé, pas besoin de labels en production)

**Seuil de détection :** 0.5234 (Percentile 95 des scores normaux sur VAL)

**Features utilisées :** 24 capteurs physiques — `fault_injection_level_pct` **EXCLUE**

---

## CHECKLIST SOUTENANCE

```
PARTIE ML (Google Colab)
  [x] Dataset chargé (199 202 obs, après déduplication)
  [x] Split temporel strict 60/20/20 (pas de fuite temporelle)
  [x] Preprocessing fit sur TRAIN uniquement (SimpleImputer + StandardScaler)
  [x] 4 modèles évalués (IF, OCSVM, LSTM, RF)
  [x] fault_injection_level_pct exclue (découverte de leakage documentée)
  [x] Modèle final : IsolationForest (non supervisé)
  [x] model_pipeline.joblib sauvegardé (2.7 MB)
  [x] metadata.json avec features + métriques

PARTIE DÉPLOIEMENT
  [x] API Flask /health /predict /predict/batch /info /scenarios
  [x] 3 scénarios testés et validés (NORMAL ✅ LIMITE ✅ ANOMALY ✅)
  [x] Flow Node-RED : MQTT → Validation → ML → InfluxDB
  [x] Dashboard Grafana : 9 panneaux
  [x] Dockerfile prêt
  [x] Git init + premier commit (14 fichiers)
  [ ] Push GitHub (à faire avec votre compte)
  [ ] InfluxDB configuré (base aeronautique_iot)
  [ ] Grafana datasource connectée
  [ ] Démonstration en direct avec Wokwi/ESP32
```

---

## EN CAS DE PROBLÈME

### L'API ne démarre pas
```powershell
# Vérifier que le modèle existe
Test-Path "c:\Users\hp\Desktop\Proj pf\iot-anomaly-detection\model\model_pipeline.joblib"
# Doit retourner : True
```

### Port 5000 déjà utilisé
```powershell
# Trouver le processus sur le port 5000
netstat -ano | findstr :5000
# Tuer le processus (remplacer PID par le numéro)
taskkill /PID <PID> /F
```

### Node-RED ne reçoit pas de MQTT
- Vérifier que le broker HiveMQ est accessible : `broker.hivemq.com:1883`
- Vérifier le topic : `aeronautique/esp32/sensors`
- Utiliser les nœuds **Inject** pour tester sans MQTT

### InfluxDB connection refused
```powershell
# Vérifier qu'InfluxDB tourne
Invoke-WebRequest http://localhost:8086/ping | Select-Object StatusCode
# Doit retourner : 204
```

### Grafana no data
- Vérifier que des données existent dans InfluxDB
- Ajuster la plage de temps (Time picker) → Last 15 minutes
- Vérifier le nom du measurement : `sensors_ml`

---

*Guide généré le 2026-08-27 | PFE IoT Aéronautique — Détection d'Anomalies ML*
