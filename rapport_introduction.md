# ═══════════════════════════════════════════════════════════════════════════════
# RAPPORT DE PROJET DE FIN D'ÉTUDES
# ═══════════════════════════════════════════════════════════════════════════════
#
# Solution embarquée IoT pour le monitoring des paramètres critiques
# aéronautiques et la détection d'anomalies
#
# Nourhen KHELIFI — CDC_2026_NourhenKHELIFI_YC_ES20268812
# YaneCode Digital — Aeronautics & Embedded Systems
# Été 2026
# ═══════════════════════════════════════════════════════════════════════════════

---

# Pages préliminaires

## Page de garde

**[À COMPLÉTER — Insérer la page de garde officielle de l'établissement]**

---

## Dédicace

**[À COMPLÉTER]**

---

## Remerciements

**[À COMPLÉTER]**

---

## Résumé

Ce projet de fin d'études porte sur la conception et le développement d'une solution embarquée IoT dédiée au monitoring des paramètres critiques aéronautiques et à la détection d'anomalies. L'architecture proposée repose sur un microcontrôleur ESP32, simulé via l'environnement Wokwi, qui assure l'acquisition de données de température (DHT22), de pression barométrique (BMP180) et d'accélération (MPU6050). Les mesures, structurées en format JSON, sont transmises en temps réel via le protocole MQTT vers un broker HiveMQ, puis routées par Node-RED vers une base de données orientée séries temporelles (InfluxDB 3 Core). La visualisation est assurée par un tableau de bord Grafana Cloud comportant dix panneaux de supervision. Un mécanisme de détection d'anomalies embarqué, fondé sur des seuils physiques, permet une réaction locale immédiate (LED, buzzer). En complément, une analyse par apprentissage automatique non supervisé (Isolation Forest, One-Class SVM, Autoencoder LSTM) est développée sur des données de télémétrie (SurveilDrone-Net23, NASA SMAP/MSL) afin de détecter des comportements atypiques complexes. L'avancement global du projet est estimé à 87 %.

**Mots-clés :** IoT, systèmes embarqués, aéronautique, ESP32, MQTT, détection d'anomalies, Machine Learning, Isolation Forest, séries temporelles, Grafana, InfluxDB.

---

## Abstract

This final year project addresses the design and development of an embedded IoT solution dedicated to the monitoring of critical aeronautical parameters and anomaly detection. The proposed architecture relies on an ESP32 microcontroller, simulated through the Wokwi environment, which acquires temperature (DHT22), barometric pressure (BMP180), and acceleration (MPU6050) data. Measurements, structured in JSON format, are transmitted in real time via the MQTT protocol to a HiveMQ broker, then routed by Node-RED to a time-series database (InfluxDB 3 Core). Visualization is handled by a Grafana Cloud dashboard featuring ten monitoring panels. An embedded anomaly detection mechanism based on physical thresholds enables immediate local reaction (LED, buzzer). Additionally, unsupervised machine learning analysis (Isolation Forest, One-Class SVM, LSTM Autoencoder) is developed on telemetry data (SurveilDrone-Net23, NASA SMAP/MSL) to detect complex atypical behaviors. The overall project advancement is estimated at 87%.

**Keywords:** IoT, embedded systems, aeronautics, ESP32, MQTT, anomaly detection, Machine Learning, Isolation Forest, time series, Grafana, InfluxDB.

---

## Liste des figures

| N° | Titre | Page |
| :--- | :--- | :--- |
| Figure 1.1 | Organigramme de YaneCode Digital | **[À COMPLÉTER]** |
| Figure 1.2 | Diagramme de Gantt du projet | **[À COMPLÉTER]** |
| Figure 2.1 | Architecture IoT trois couches | **[À COMPLÉTER]** |
| Figure 2.2 | Comparaison des cartes embarquées | **[À COMPLÉTER]** |
| Figure 2.3 | Schéma fonctionnel du protocole MQTT | **[À COMPLÉTER]** |
| Figure 3.1 | Diagramme de contexte du système | **[À COMPLÉTER]** |
| Figure 3.2 | Diagramme de cas d'utilisation | **[À COMPLÉTER]** |
| Figure 3.3 | Architecture globale de la solution | **[À COMPLÉTER]** |
| Figure 3.4 | Architecture matérielle détaillée | **[À COMPLÉTER]** |
| Figure 3.5 | Diagramme de séquence — acquisition à l'affichage | **[À COMPLÉTER]** |
| Figure 4.1 | Montage Wokwi — circuit complet | **[À COMPLÉTER]** |
| Figure 4.2 | Flux Node-RED | **[À COMPLÉTER]** |
| Figure 4.3 | Dashboard Grafana — 10 panneaux | **[À COMPLÉTER]** |
| Figure 5.1 | Distribution des comportements de surveillance | **[À COMPLÉTER]** |
| Figure 5.2 | Répartition Normal / Anomalie | **[À COMPLÉTER]** |
| Figure 5.3 | Température avec anomalies marquées | **[À COMPLÉTER]** |
| Figure 5.4 | Vibration RMS avec seuil 95 % | **[À COMPLÉTER]** |
| Figure 5.5 | Heatmap de corrélation | **[À COMPLÉTER]** |
| Figure 5.6 | Espace PCA 2D | **[À COMPLÉTER]** |
| Figure 5.7 | Architecture de l'Autoencoder LSTM | **[À COMPLÉTER]** |
| Figure 5.8 | Courbes ROC — comparaison des trois modèles | **[À COMPLÉTER]** |
| Figure 5.9 | Courbes Precision-Recall | **[À COMPLÉTER]** |
| Figure 5.10 | Matrices de confusion | **[À COMPLÉTER]** |
| Figure 5.11 | Validation NASA SMAP/MSL | **[À COMPLÉTER]** |
| Figure 5.12 | Simulation flux MQTT temps réel | **[À COMPLÉTER]** |

---

## Liste des tableaux

| N° | Titre | Page |
| :--- | :--- | :--- |
| Tableau 1.1 | Fiche signalétique de YaneCode Digital | **[À COMPLÉTER]** |
| Tableau 1.2 | Comparaison des solutions IoT existantes | **[À COMPLÉTER]** |
| Tableau 1.3 | Cahier des charges — besoins fonctionnels | **[À COMPLÉTER]** |
| Tableau 1.4 | Cahier des charges — besoins non fonctionnels | **[À COMPLÉTER]** |
| Tableau 2.1 | Comparaison des cartes embarquées | **[À COMPLÉTER]** |
| Tableau 2.2 | Comparaison des capteurs | **[À COMPLÉTER]** |
| Tableau 2.3 | Comparaison des protocoles de communication | **[À COMPLÉTER]** |
| Tableau 2.4 | Comparaison des bases de données | **[À COMPLÉTER]** |
| Tableau 2.5 | Comparaison des outils de visualisation | **[À COMPLÉTER]** |
| Tableau 3.1 | Besoins fonctionnels détaillés | **[À COMPLÉTER]** |
| Tableau 3.2 | Besoins non fonctionnels détaillés | **[À COMPLÉTER]** |
| Tableau 3.3 | Identification des acteurs | **[À COMPLÉTER]** |
| Tableau 4.1 | Environnement matériel et logiciel | **[À COMPLÉTER]** |
| Tableau 4.2 | Configuration des capteurs | **[À COMPLÉTER]** |
| Tableau 4.3 | Problèmes rencontrés et solutions | **[À COMPLÉTER]** |
| Tableau 4.4 | Résultats des tests de validation | **[À COMPLÉTER]** |
| Tableau 4.5 | Scénarios d'anomalie testés | **[À COMPLÉTER]** |
| Tableau 5.1 | Description des datasets | **[À COMPLÉTER]** |
| Tableau 5.2 | Features d'ingénierie | **[À COMPLÉTER]** |
| Tableau 5.3 | Comparaison des modèles ML | **[À COMPLÉTER]** |
| Tableau 5.4 | Avancement global du projet | **[À COMPLÉTER]** |

---

## Liste des acronymes

| Acronyme | Signification |
| :--- | :--- |
| ADC | Analog-to-Digital Converter |
| AE | Autoencoder |
| API | Application Programming Interface |
| AUC | Area Under the Curve |
| BLE | Bluetooth Low Energy |
| CDC | Cahier des Charges |
| EDA | Exploratory Data Analysis |
| ESP | Espressif Systems Processor |
| GPIO | General Purpose Input/Output |
| gRPC | Google Remote Procedure Call |
| hPa | Hectopascal |
| HTTP | HyperText Transfer Protocol |
| I2C | Inter-Integrated Circuit |
| IF | Isolation Forest |
| IoT | Internet of Things |
| JSON | JavaScript Object Notation |
| LCD | Liquid Crystal Display |
| LED | Light-Emitting Diode |
| LOF | Local Outlier Factor |
| LSTM | Long Short-Term Memory |
| ML | Machine Learning |
| MQTT | Message Queuing Telemetry Transport |
| MSE | Mean Squared Error |
| NTP | Network Time Protocol |
| OCSVM | One-Class Support Vector Machine |
| PCA | Principal Component Analysis |
| PFE | Projet de Fin d'Études |
| PR-AUC | Precision-Recall Area Under the Curve |
| QoS | Quality of Service |
| RAM | Random Access Memory |
| RMS | Root Mean Square |
| ROC | Receiver Operating Characteristic |
| SDA | Serial Data Line |
| SCL | Serial Clock Line |
| SHAP | SHapley Additive exPlanations |
| SMAP | Soil Moisture Active Passive |
| MSL | Mars Science Laboratory |
| SVM | Support Vector Machine |
| TLS | Transport Layer Security |
| TSDB | Time Series Database |
| UAV | Unmanned Aerial Vehicle |
| UML | Unified Modeling Language |
| UART | Universal Asynchronous Receiver-Transmitter |
| XAI | Explainable Artificial Intelligence |

---

## Table des matières

**[À GÉNÉRER AUTOMATIQUEMENT DANS WORD/LATEX]**

---

# INTRODUCTION GÉNÉRALE

## 1. Contexte général

La transformation numérique des industries critiques constitue l'un des enjeux majeurs de l'ingénierie contemporaine. Dans le secteur aéronautique, la sûreté de fonctionnement et la disponibilité opérationnelle des systèmes reposent historiquement sur des programmes de maintenance préventive systématique, fondés sur des calendriers rigides et des inspections visuelles périodiques. Toutefois, ces approches traditionnelles présentent des limites intrinsèques : elles ne tiennent pas compte de l'état réel du système entre deux interventions et génèrent des coûts d'immobilisation significatifs.

L'émergence de l'Internet des Objets (IoT) industriel offre une alternative prometteuse. Grâce à des réseaux de capteurs embarqués, il est désormais possible d'acquérir en continu des paramètres physiques — température, pression, vibration, altitude — et de les transmettre vers des plateformes de traitement et de visualisation. Cette capacité de monitoring en temps réel constitue le socle de la maintenance conditionnelle, voire prédictive, qui vise à intervenir uniquement lorsque l'état du système l'exige, réduisant ainsi les coûts opérationnels tout en améliorant la sécurité.

## 2. Problématique

Les systèmes aéronautiques sont caractérisés par des comportements dynamiques complexes, où les anomalies peuvent se manifester sous des formes variées : dérives lentes d'un paramètre, pics soudains, corrélations inhabituelles entre plusieurs grandeurs physiques. La simple surveillance par dépassement de seuils statiques, bien qu'indispensable pour les situations d'urgence, s'avère insuffisante pour détecter les prémices d'une défaillance. La problématique se formule donc ainsi : **comment concevoir une solution embarquée IoT capable de collecter et de surveiller des paramètres critiques aéronautiques, de détecter localement et à distance les anomalies, et de visualiser l'état du système de manière fiable et efficace ?**

## 3. Motivation

La motivation de ce projet réside dans la convergence de plusieurs avancées technologiques complémentaires. Les microcontrôleurs modernes, tels que l'ESP32, offrent une puissance de calcul suffisante pour un premier niveau de traitement embarqué (filtrage, détection par seuils), tout en intégrant nativement une connectivité Wi-Fi. Le protocole MQTT, conçu spécifiquement pour les environnements IoT contraints, permet une transmission légère et asynchrone des données. Les bases de données orientées séries temporelles (InfluxDB) et les outils de visualisation (Grafana) constituent un écosystème mature pour le monitoring. Enfin, les méthodes d'apprentissage automatique non supervisé (Isolation Forest, Autoencoder LSTM) permettent de détecter des comportements atypiques sans nécessiter un corpus exhaustif d'anomalies labellisées, ce qui est particulièrement pertinent dans le domaine aéronautique où les défaillances sont, par nature, rares.

## 4. Objectifs du projet

L'objectif principal de ce projet de fin d'études est de concevoir, d'implémenter et de valider une chaîne IoT complète, depuis le capteur embarqué jusqu'au tableau de bord de supervision, en passant par une couche d'intelligence artificielle pour la détection d'anomalies. Les objectifs spécifiques sont les suivants :

1. **Définir les paramètres critiques** à surveiller et justifier leur pertinence aéronautique (température, pression, vibration).
2. **Concevoir l'acquisition** des données à l'aide de capteurs embarqués (DHT22, BMP180, MPU6050) sur un microcontrôleur ESP32, en intégrant un filtrage numérique (moyenne glissante).
3. **Implémenter la transmission** fiable des mesures via le protocole MQTT vers un broker (HiveMQ).
4. **Mettre en place le stockage** temporel des données dans InfluxDB et la **visualisation** en temps réel via Grafana.
5. **Développer une détection d'anomalies** à deux niveaux : embarquée (seuils physiques) et serveur (Machine Learning non supervisé).
6. **Valider le système** à travers trois scénarios : nominal, limite et anomalie.

## 5. Méthodologie adoptée

La méthodologie adoptée s'appuie sur un processus itératif et incrémental, structuré en cinq phases :
- **Phase 1 — Étude et benchmarking** : Revue de l'état de l'art, comparaison des technologies (cartes, capteurs, protocoles, bases de données).
- **Phase 2 — Conception** : Définition de l'architecture matérielle et logicielle, modélisation UML.
- **Phase 3 — Implémentation matérielle (Edge)** : Développement du firmware ESP32 en C++, simulation via Wokwi, validation du circuit.
- **Phase 4 — Déploiement de la chaîne IoT** : Configuration de MQTT, Node-RED, InfluxDB et Grafana, résolution des problèmes d'intégration.
- **Phase 5 — Analyse de données et ML** : Exploration des datasets de télémétrie, ingénierie des features, entraînement et évaluation des modèles de détection d'anomalies.

## 6. Organisation du rapport

Le présent rapport s'articule autour de cinq chapitres, complétés par une conclusion générale et des annexes :

- **Le Chapitre 1** présente le contexte général du projet, l'organisme d'accueil (YaneCode Digital), l'étude et la critique de l'existant, ainsi que le cahier des charges complet.
- **Le Chapitre 2** expose l'état de l'art technologique et justifie chaque choix retenu : carte embarquée, capteurs, protocole de communication, base de données et outil de visualisation.
- **Le Chapitre 3** décrit l'analyse des besoins et la conception de la solution, incluant l'identification des acteurs, l'architecture détaillée et la modélisation UML.
- **Le Chapitre 4** détaille la réalisation et l'implémentation du système, couvrant le firmware ESP32, la communication MQTT, le stockage InfluxDB, le dashboard Grafana, ainsi que les problèmes techniques rencontrés et les tests de validation.
- **Le Chapitre 5** est consacré à la détection des anomalies par apprentissage automatique, à l'analyse exploratoire des données, aux résultats et à la discussion.

Enfin, la **conclusion générale** synthétise les contributions du projet, identifie ses limites et propose des perspectives d'amélioration.

---
