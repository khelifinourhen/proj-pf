# ✈️ Système IoT & Machine Learning pour la Maintenance Prédictive Aéronautique
> **Projet de Fin d'Études (PFE 2026)** — Détection d'anomalies en temps réel et maintenance prédictive pour capteurs IoT aéronautiques.

---

## 📌 Vue d'Ensemble du Projet

Ce projet propose une solution complète et de bout-en-bout (*End-to-End*) combinant **l'Internet des Objets (IoT)** et le **Machine Learning (ML)** pour la surveillance et la détection d'anomalies sur des capteurs aéronautiques (vibrations, température, pression, régime moteur).

`
┌─────────────────────────┐       HTTP / JSON       ┌─────────────────────────┐
│   ESP32 Edge (Wokwi)    │ ──────────────────────> │    API Backend Flask    │
│  Simulation Capteurs    │                         │  Prétraitement & ML     │
└─────────────────────────┘                         └────────────┬────────────┘
                                                                 │
                                                                 ▼
┌─────────────────────────┐       Telemetry         ┌─────────────────────────┐
│   Node-RED & Grafana    │ <────────────────────── │ Modèle Isolation Forest │
│  Tableaux de Bord       │                         │ Détection & Scoring     │
└─────────────────────────┘                         └─────────────────────────┘
`

---

## 🗂️ Structure du Répertoire

- **wokwi-vscode/** : Code source embarqué ESP32 (Arduino C++ sketch.ino), diagramme Wokwi et bibliothèques de simulation.
- **iot-anomaly-detection/** :
  - **pi/** : API REST Flask (pp.py, pp_flask.py) pour l'ingestion et l'inférence.
  - **model/** : Modèles pré-entraînés (*Isolation Forest*, Scaler, Imputer).
  - **
ode-red/** : Flux Node-RED (lows.json) pour l'orchestration des données.
  - **grafana/** : Configuration et dashboards Grafana pour la visualisation temps réel.
  - **Dockerfile & ender.yaml** : Fichiers de conteneurisation et de déploiement cloud (Render.com).
- **
otebooks/ & scripts ML** : Scripts d'entraînement (	rain_and_save_pipeline.py, un_final_audit.py) et notebooks Jupyter d'analyse exploratoire et d'évaluation.
- **Documentation Académique** :
  - RAPPORT_PFE_COMPLET.md : Rapport complet de PFE structuré par chapitres.
  - diagrammes_UML_corriges.md : Diagrammes de cas d'utilisation, séquence, classes et composants.
  - presentation_avancement_PFE.md : Support de présentation et soutenance.

---

## 🚀 Démarrage Rapide

### 1. Démarrer l'API Backend
`ash
cd iot-anomaly-detection/api
pip install -r requirements.txt
python app.py
`
L'API est accessible sur http://localhost:5000 (ou port configuré) avec les endpoints /health, /predict, /stats.

### 2. Lancer la Simulation ESP32
Ouvrez le dossier wokwi-vscode/ sous VS Code avec l'extension **Wokwi for VS Code** et lancez la simulation via diagram.json.

### 3. Entraîner les Modèles ML
`ash
python train_and_save_pipeline.py
`

---

## 👥 Auteur
- **Nourhen Khelifi** — Projet de Fin d'Études 2026
