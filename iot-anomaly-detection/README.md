# IoT Anomaly Detection - PFE 2025/2026

> **Solution embarquee IoT pour le monitoring des parametres critiques aeronautiques et la detection d anomalies**
> Etudiant : Nourhen KHELIFI | Encadrant : Dr. Et Tousy Jamal

---

## Architecture de la Solution

```
ESP32 / Capteurs (Wokwi)
        |
        | MQTT (HiveMQ)
        v
     Node-RED
   Parse + Validate
        |
        | HTTP POST
        v
  Service Python ML          <- modele Isolation Forest
  FastAPI /predict           <- preprocessing inclus dans le pipeline
        |
        | JSON {anomaly, score, status}
        v
     Node-RED
   Fusion donnees
        |
        v
     InfluxDB
  measurement: sensors_ml
        |
        v
     Grafana
  Dashboard + Alertes
```

## Modele ML

| Propriete | Valeur |
|---|---|
| Algorithme | Isolation Forest |
| Type | Non supervise - detection d anomalies |
| Features | 24 (capteurs physiques uniquement) |
| Pipeline | SimpleImputer + StandardScaler + IsolationForest |
| Seuil | Percentile 95 sur donnees normales de validation |
| ROC-AUC (test) | 0.6937 |
| Dataset | 199 202 observations (60/20/20 split temporel) |
| Variable cible | anomaly_reference |
| Variables interdites | fault_injection_level_pct, failure_type, failure_event |

## Structure du Projet

```
iot-anomaly-detection/
+-- api/
|   +-- app.py              <- FastAPI /health /predict /predict/batch /info /scenarios
|   +-- requirements.txt
+-- model/
|   +-- model_pipeline.joblib   <- Pipeline Sklearn (imputer + scaler + IF)
|   +-- if_config.joblib        <- seuil + contamination
|   +-- metadata.json           <- features, metriques, version
+-- node-red/
|   +-- flow.json           <- Flux Node-RED complet
+-- grafana/
|   +-- dashboard.json      <- Dashboard 9 panneaux
+-- tests/
|   +-- test_api.py         <- Tests pytest
+-- notebooks/
|   +-- training.ipynb      <- Notebook Google Colab
+-- train_and_save_pipeline.py  <- Script d entrainement
+-- Dockerfile
+-- .gitignore
+-- README.md
```

## Installation et Lancement

### 1. Cloner le depot
```bash
git clone https://github.com/VOTRE_USERNAME/iot-anomaly-detection.git
cd iot-anomaly-detection
```

### 2. Creer l environnement Python
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r api/requirements.txt
```

### 3. Lancer l API
```bash
uvicorn api.app:app --host 0.0.0.0 --port 5000 --reload
```

### 4. Verifier que l API fonctionne
```bash
curl http://localhost:5000/health
```
Reponse attendue :
```json
{"status": "ok", "model_loaded": true, "uptime_seconds": 1.2}
```

### 5. Tester la prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature_c": 25.4, "pressure_hpa": 1012.5, "vibration_norm_ms2": 0.15}'
```
Reponse :
```json
{
  "anomaly": 0,
  "anomaly_score": 0.4812,
  "status": "NORMAL",
  "model": "IsolationForest",
  "threshold": 0.523398,
  "timestamp": "2026-08-27T17:00:00.000Z",
  "message": "Comportement normal"
}
```

## API Endpoints

| Methode | Endpoint | Description |
|---|---|---|
| GET | /health | Status de l API + statistiques |
| GET | /info | Informations sur le modele |
| GET | /scenarios | Donnees de test pour les 3 scenarios |
| POST | /predict | Prediction sur 1 observation |
| POST | /predict/batch | Prediction sur N observations |

## Deploiement Docker

```bash
docker build -t anomaly-api .
docker run -p 5000:5000 anomaly-api
```

## Integration Node-RED

1. Importer `node-red/flow.json` dans Node-RED (Menu > Import)
2. Configurer le broker MQTT (hivemq-broker) avec votre adresse HiveMQ
3. Configurer InfluxDB avec votre adresse locale
4. Deployer le flux
5. L API doit etre lancee sur localhost:5000

## 3 Scenarios de Test

### Scenario 1 - Nominal
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" \
  -d '{"temperature_c":24.5,"pressure_hpa":1013.0,"humidity_pct":52.0,"vibration_norm_ms2":0.12,"voltage_v":3.3,"rpm":1450.0}'
```
Resultat attendu : `"status": "NORMAL"`

### Scenario 2 - Limite
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" \
  -d '{"temperature_c":68.0,"pressure_hpa":980.0,"vibration_norm_ms2":1.8,"voltage_v":3.1,"rpm":2800.0}'
```
Resultat : variable selon le modele (surveillance recommandee)

### Scenario 3 - Anomalie
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" \
  -d '{"temperature_c":142.0,"pressure_hpa":650.0,"vibration_norm_ms2":15.3,"voltage_v":2.4,"rpm":5500.0}'
```
Resultat attendu : `"status": "ANOMALY"`

## Tests

```bash
pip install pytest
pytest tests/test_api.py -v
```

## Grafana

Importer `grafana/dashboard.json` via Grafana > Dashboards > Import.
Configurer la datasource InfluxDB avec la base `aeronautique_iot`.

Panneaux disponibles :
- Statut NORMAL / ANOMALY (temps reel)
- Score d anomalie (serie temporelle)
- Nombre d anomalies (fenetre glissante)
- Temperature, Pression, Vibrations, Voltage, RPM
- Tableau des dernieres anomalies detectees

## Checklist Soutenance

- [x] Dataset charge et explore (199 202 observations)
- [x] Split temporel 60/20/20 sans leakage
- [x] Preprocessing fit uniquement sur TRAIN
- [x] Isolation Forest entraine et valide
- [x] model_pipeline.joblib sauvegarde
- [x] metadata.json avec features et metriques
- [x] API FastAPI avec /health /predict /info /scenarios
- [x] Tests pytest (7 classes de tests)
- [x] Flow Node-RED avec validation + preparation ML + gestion erreurs
- [x] Dashboard Grafana 9 panneaux
- [x] Dockerfile pour containerisation
- [x] README avec guide complet
- [x] 3 scenarios de test documentes

## Licence

MIT - Projet PFE 2025/2026
