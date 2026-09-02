# 🧠 Serveur API Backend & Inférence ML

Service REST d'inférence en temps réel basé sur **Flask** et **FastAPI**, chargeant le modèle **Isolation Forest** pré-entraîné pour la détection d'anomalies sur les flux capteurs.

## 📁 Contenu
- pp_flask.py : Serveur Flask principal (endpoints /predict, /health, /stats).
- pp.py : Version alternative FastAPI avec validation Pydantic et Swagger UI (/docs).
- equirements.txt : Dépendances Python nécessaires.
- Dockerfile : Conteneur de production Docker.
- ender.yaml & Procfile : Configurations de déploiement automatique sur **Render.com**.
- model/ : Modèles sérialisés (model_pipeline.joblib, if_config.joblib, metadata.json, etc.).
- 	ests/ : Tests unitaires et d'intégration (	est_api.py, 	est_scenarios.py).

## 💻 Exécution Locale
`ash
cd api-ml-backend
pip install -r requirements.txt
python app_flask.py
`
L'API écoute sur http://localhost:5000.

## ☁️ Déploiement Cloud Gratuit (Render.com)
1. Créez un compte gratuit sur [Render.com](https://render.com/).
2. Cliquez sur **New +** > **Web Service**.
3. Liez votre dépôt GitHub khelifinourhen/iot-anomaly-detection.
4. Spécifiez le Root Directory : pi-ml-backend.
5. Build Command : pip install -r requirements.txt
6. Start Command : python app_flask.py
"@ | Out-File -FilePath "C:\Users\hp\Documents\Github\proj pf\api-ml-backend\README.md" -Encoding utf8

@"
FROM nodered/node-red:latest
COPY flows.json /data/flows.json
