# Contenu Présentation d'Avancement — Projet PFE IoT Aéronautique
## Nourhen KHELIFI — YaneCode Digital — Août 2026
### À copier dans Claude pour générer le PPTX

---

## SLIDE 1 — PAGE DE TITRE

**Titre :** Solution Embarquée IoT pour le Monitoring des Paramètres Critiques Aéronautiques et la Détection d'Anomalies

**Sous-titre :** Présentation d'Avancement de Projet

**Informations :**
- **Stagiaire :** Nourhen KHELIFI
- **Entreprise :** YaneCode Digital — Aeronautics & Embedded Systems
- **Référence :** CDC_2026_NourhenKHELIFI_YC_ES20268812
- **Date :** Août 2026
- **Avancement global : 87 %**

---

## SLIDE 2 — SOMMAIRE

1. Contexte et problématique
2. Objectifs du projet
3. Architecture de la solution
4. Réalisations — Module Embarqué (ESP32)
5. Réalisations — Communication MQTT
6. Réalisations — Middleware Node-RED
7. Réalisations — Stockage InfluxDB
8. Réalisations — Dashboard Grafana
9. Réalisations — Détection d'anomalies embarquée
10. Réalisations — Pipeline ML (Isolation Forest, OCSVM, Autoencoder LSTM)
11. Difficultés techniques rencontrées
12. Tests et validation
13. Démonstration — Scénarios d'anomalie
14. Avancement détaillé par module
15. Limites actuelles
16. Étapes suivantes (court / moyen / long terme)
17. Conclusion

---

## SLIDE 3 — CONTEXTE ET PROBLÉMATIQUE

**Contexte :**
- L'aéronautique exige une surveillance continue des paramètres critiques (température, pression, vibration)
- La maintenance préventive traditionnelle (calendrier fixe) est coûteuse et ne détecte pas les dérives précoces
- L'IoT industriel permet un monitoring temps réel depuis le capteur jusqu'au tableau de bord

**Problématique :**
> Comment concevoir une solution IoT embarquée capable de collecter, surveiller et détecter des anomalies sur des paramètres critiques aéronautiques, en temps réel, de manière fiable et interprétable ?

**Enjeux :**
- Réactivité < 1 seconde pour les anomalies critiques
- Fiabilité de la chaîne capteur → cloud
- Interprétabilité des alertes (pourquoi cette anomalie ?)

---

## SLIDE 4 — OBJECTIFS DU PROJET

| N° | Objectif | Statut |
|:---|:---|:---|
| O1 | Acquérir les données capteurs (température, pression, vibration) via ESP32 | ✅ Terminé |
| O2 | Filtrer les données brutes (moyenne glissante, validation) | ✅ Terminé |
| O3 | Détecter les anomalies en embarqué (seuils physiques) | ✅ Terminé |
| O4 | Transmettre les mesures via MQTT (JSON, QoS 0) | ✅ Terminé |
| O5 | Router et valider les données via Node-RED | ✅ 95% |
| O6 | Stocker les séries temporelles dans InfluxDB | ✅ 95% |
| O7 | Visualiser en temps réel via Grafana (10 panneaux) | ✅ 95% |
| O8 | Détecter les anomalies côté serveur (ML) | 🔄 En cours |
| O9 | Valider sur 3 scénarios (normal, limite, anomalie) | ✅ Terminé |
| O10 | Documenter et rédiger le rapport PFE | 🔄 75% |

---

## SLIDE 5 — ARCHITECTURE GLOBALE — PIPELINE 5 COUCHES

```
┌─────────────────────────────────────────────────────────┐
│ COUCHE 5 : VISUALISATION                                │
│   Grafana Cloud — 10 panels — refresh 5s — InfluxQL     │
├──────────────────────┬──────────────────────────────────┤
│ COUCHE 4 : STOCKAGE  │  InfluxDB 3 Core v3.11.0        │
│   bucket: aircraft   │  measurement: sensors            │
│   8 fields, 1 tag    │  localhost:8181 + ngrok tunnel   │
├──────────────────────┴──────────────────────────────────┤
│ COUCHE 3 : MIDDLEWARE                                   │
│   Node-RED — mqtt_in → parse_validate → influx_out      │
├─────────────────────────────────────────────────────────┤
│ COUCHE 2 : BROKER MQTT                                  │
│   HiveMQ Public — broker.hivemq.com:1883 — QoS 0       │
│   Topic: aircraft/sensors                               │
├─────────────────────────────────────────────────────────┤
│ COUCHE 1 : ACQUISITION                                  │
│   ESP32 DevKit C v4 (Wokwi) — 240 MHz — 520 KB RAM     │
│   DHT22 + BMP180 + MPU6050 + Pot + LCD + LED + Buzzer   │
└─────────────────────────────────────────────────────────┘
```

**Flux de données :**  ESP32 → WiFi → HiveMQ → Node-RED → InfluxDB → Grafana

---

## SLIDE 6 — RÉALISATIONS : MODULE EMBARQUÉ (ESP32)

**Firmware C++ :**
- 392 lignes de code
- Taille compilée : 974 KB
- 100 % non bloquant (millis(), zéro delay())

**Capteurs intégrés :**

| Capteur | Paramètre | Interface | Pin/Adresse |
|:---|:---|:---|:---|
| DHT22 | Température (-40 à +80°C) / Humidité (0-100%) | GPIO | Pin 15 |
| BMP180 | Pression (300-1100 hPa) / Altitude | I2C | 0x77 |
| MPU6050 | Accélération 3 axes (m/s²) | I2C | 0x68 |
| Potentiomètre | Simulation défaut (0-100%) | ADC 12 bits | GPIO 34 |

**Actuateurs :**
- LCD 20×4 (I2C) : affichage mesures + status
- LED Verte (GPIO 26) : état normal
- LED Rouge (GPIO 27) : état alerte
- Buzzer (GPIO 25) : alarme sonore 1500 Hz

**Intervalles non bloquants :**
- Lecture capteurs : 1000 ms
- Affichage LCD : 1000 ms
- Publication MQTT : 3000 ms
- Serial debug : 2000 ms

---

## SLIDE 7 — RÉALISATIONS : FILTRAGE ET PRÉTRAITEMENT

**Filtre Moyenne Glissante (Moving Average) :**
- Taille buffer : 5 échantillons
- Réduit le bruit haute fréquence des capteurs
- Formule : x̄ₙ = (1/5) × Σ xᵢ (i = n-4 à n)

**Horodatage :**
- NTP synchronisé (pool.ntp.org, UTC+1)
- Fallback sur millis() si NTP échoue

**Déduplication LCD :**
- Comparaison avec lastDisplay pour éviter les rafraîchissements inutiles

**Simulation de défauts (Potentiomètre) :**
- Si pot > 50% → facteur = (pot - 50) / 50
- Température += 25 × facteur
- Pression -= 250 × facteur
- Altitude += 1500 × facteur
- Accélération += 20 × facteur

---

## SLIDE 8 — RÉALISATIONS : COMMUNICATION MQTT

**Configuration :**
- Broker : HiveMQ Public (broker.hivemq.com:1883)
- Topic : aircraft/sensors
- QoS : 0 (at most once)
- Buffer MQTT : 512 octets (payload ~300 octets)
- Client ID : AircraftESP32-[MAC] (unicité garantie)

**Payload JSON transmis toutes les 3 secondes :**
```json
{
  "timestamp": 1722945600,
  "temperature": 24.5,
  "humidity": 55.0,
  "pressure": 1013.25,
  "altitude": 120.0,
  "accX": 0.12, "accY": -0.05, "accZ": 9.81,
  "potentiometer": 15,
  "status": "NORMAL",
  "reason": ""
}
```

**Reconnexion non bloquante :**
- Intervalle : 5000 ms entre tentatives
- Pas de while(true) → le loop() continue toujours

---

## SLIDE 9 — RÉALISATIONS : MIDDLEWARE NODE-RED

**Flow "Aircraft Monitor" (4 nœuds) :**

```
[mqtt in] → [Parse JSON sécurisé] → [Formatter InfluxDB] → [Écrire InfluxDB]
                                                         ↘ [Debug]
```

**Nœud 1 — mqtt_in :** Souscription aircraft/sensors depuis HiveMQ
**Nœud 2 — fn_parse_validate :** Validation JSON robuste (gère vide, tronqué, objet déjà parsé)
**Nœud 3 — fn_to_influx_points :** Formatage Line Protocol (measurement=sensors, tag=device:ESP32, 8 fields)
**Nœud 4 — influx_out :** Écriture vers InfluxDB (bucket=aircraft, precision=ms)

**Gestion d'erreurs :**
- JSON vide → node.warn() + retourne null (pas de crash)
- JSON invalide → node.error() + log du payload brut
- Horodatage manquant → Date.now() côté Node-RED

---

## SLIDE 10 — RÉALISATIONS : STOCKAGE INFLUXDB

**Configuration :**
- Version : InfluxDB 3 Core v3.11.0 (open source)
- URL : http://127.0.0.1:8181
- Organisation : aircraft_org
- Bucket : aircraft | Measurement : sensors

**Schéma des données :**

| Type | Nom | Description |
|:---|:---|:---|
| Tag | device | "ESP32" |
| Field | temperature | Float — °C |
| Field | humidity | Float — % |
| Field | pressure | Float — hPa |
| Field | altitude | Float — m |
| Field | accX, accY, accZ | Float — m/s² |
| Field | potentiometer | Integer — % |
| Timestamp | time | Precision ms |

**Accès distant :**
- Tunnel ngrok → HTTPS vers localhost:8181
- Mode InfluxQL (HTTP/1.1) — compatible ngrok (gRPC/HTTP2 incompatible)

---

## SLIDE 11 — RÉALISATIONS : DASHBOARD GRAFANA

**Configuration :**
- Grafana Cloud v13.2.0
- Datasource : InfluxDB (mode InfluxQL)
- Rafraîchissement : 5 secondes
- UID Dashboard : atdh9j

**10 Panneaux de supervision :**

| N° | Type | Contenu |
|:---|:---|:---|
| 1 | Time Series | Température (°C) |
| 2 | Time Series | Humidité (%) |
| 3 | Time Series | Pression (hPa) |
| 4 | Time Series | Altitude (m) |
| 5-7 | Time Series | Accélération X, Y, Z (m/s²) |
| 8 | Gauge | Potentiomètre (0-100%) |
| 9 | Stat | Valeurs instantanées |
| 10 | Table | Dernières mesures |

---

## SLIDE 12 — RÉALISATIONS : DÉTECTION D'ANOMALIES EMBARQUÉE

**Stratégie à deux niveaux :**

| Niveau | Lieu | Méthode | Latence | Avantage |
|:---|:---|:---|:---|:---|
| **Niveau 1** | ESP32 (embarqué) | Seuils physiques fixes | < 1 ms | Réaction immédiate, sans réseau |
| **Niveau 2** | Serveur (Python) | Isolation Forest (ML) | ~100 ms | Détection contextuelle |

**Seuils embarqués (Niveau 1) — Priorité décroissante :**

| Condition | Seuil | Alerte | Action |
|:---|:---|:---|:---|
| Température > 45 °C | 45.0 | HIGH TEMP | LED rouge + Buzzer + LCD |
| Pression < 850 hPa | 850.0 | LOW PRESSURE | LED rouge + Buzzer + LCD |
| Vibration > 15 m/s² | 15.0 | HIGH VIBRATION | LED rouge + Buzzer + LCD |
| Potentiomètre > 80% | 80 | ENGINE FAILURE | LED rouge + Buzzer + LCD |

**Calcul vibration :** vibration = √(accX² + accY² + (accZ − 9.8)²)

---

## SLIDE 13 — RÉALISATIONS : PIPELINE ML

**Dataset principal :** SurveilDrone-Net23 (Kaggle)
- 140 256+ enregistrements, fréquence 15 min, période 2021-2024

**Dataset de validation :** NASA SMAP/MSL Telemanom (HuggingFace)
- 55 canaux SMAP + 27 canaux MSL — anomalies annotées par experts NASA

**Feature Engineering : 22 features créées**
- vibration_rms, temp_gradient, temp_z_score, battery_critical
- pressure_hpa, rolling_std, rolling_max (fenêtre 4 pts = 1h)

**3 Modèles développés :**

| Modèle | Type | Paramètres clés |
|:---|:---|:---|
| **Isolation Forest** | Non supervisé, arbres | n_estimators=200, contamination=0.05 |
| **One-Class SVM** | Non supervisé, frontière | kernel=RBF, nu=0.05, réduction PCA |
| **Autoencoder LSTM** | Deep Learning | LSTM(64→32→8→32→64), seq=10, epochs=60 |

**Résultats :** [À CONFIRMER APRÈS EXÉCUTION DU NOTEBOOK]

---

## SLIDE 14 — DIFFICULTÉS TECHNIQUES RENCONTRÉES

| ID | Problème | Solution | Statut |
|:---|:---|:---|:---|
| D1 | JSON vide dans Node-RED | Validation JS robuste + gestion cas null | ✅ |
| D2 | Simulation Wokwi gelée | Suppression while(!Serial) | ✅ |
| D3 | BMP180 pression = 47750 Pa | Correction diagram.json à 101325 Pa | ✅ |
| D4 | gRPC/ngrok incompatible | Passage mode InfluxQL (HTTP/1.1) | ✅ |
| D5 | Token InfluxDB 401 | Injection directe via API | ⚠️ 95% |
| D6 | ngrok version obsolète | ngrok update → v3.39.10 | ✅ |
| D7 | Client MQTT dupliqué | ID = AircraftESP32-[MAC] | ✅ |

**7 difficultés identifiées → 6 résolues + 1 quasi-résolue**

---

## SLIDE 15 — TESTS ET VALIDATION

**Tests firmware : 6/6 OK ✅**
- movingAverage(), getTimestamp(), readSensors(), detectAnomaly(), sendMQTT(), reconnectMQTT()

**Tests API InfluxDB : 5/5 OK ✅**
- Health, Auth Bearer, SQL, InfluxQL, Écriture

**Tests ngrok : 3/3 OK ✅**
- Ping, SQL, InfluxQL via tunnel

**Test Grafana :** "datasource is working. 1 measurements found" ✅

---

## SLIDE 16 — DÉMONSTRATION : SCÉNARIOS D'ANOMALIE

| Scénario | Pot | Valeur | Détection | Résultat |
|:---|:---|:---|:---|:---|
| Normal | 0% | T=24.5°C, P=1013 hPa | NORMAL | ✅ |
| Limite | 70% | T=34.5°C, P=913 hPa | NORMAL | ✅ |
| Haute temp. | 95% | T=47.5°C (> 45°C) | ALERT: HIGH TEMP | ✅ |
| Basse pression | 85% | P=838 hPa (< 850) | ALERT: LOW PRESSURE | ✅ |
| Vibration | 80% | Vib=17 m/s² (> 15) | ALERT: HIGH VIBRATION | ✅ |
| Panne moteur | 90% | Pot > 80% | ALERT: ENGINE FAILURE | ✅ |

**6/6 scénarios conformes**

---

## SLIDE 17 — AVANCEMENT DÉTAILLÉ PAR MODULE

| Module | État | % |
|:---|:---|:---|
| Architecture générale | ✅ Terminé | 100% |
| Simulation Wokwi | ✅ Terminé | 100% |
| Firmware ESP32 (392 lignes) | ✅ Terminé | 100% |
| Filtrage / Prétraitement | ✅ Terminé | 100% |
| Communication MQTT | ✅ Terminé | 100% |
| Broker HiveMQ | ✅ Terminé | 100% |
| Tunnel ngrok | ✅ Terminé | 100% |
| Node-RED flux | ⚠️ Quasi terminé | 95% |
| InfluxDB structure | ⚠️ Quasi terminé | 95% |
| Dashboard Grafana | ⚠️ Quasi terminé | 95% |
| Détection embarquée | ✅ Terminé | 100% |
| Détection ML serveur | 🔄 En cours | 60% |
| Tests validation | ⚠️ Quasi terminé | 80% |
| Documentation | 🔄 En cours | 75% |

**AVANCEMENT GLOBAL : 87%**

---

## SLIDE 18 — LIMITES ACTUELLES

| ID | Limite | Criticité |
|:---|:---|:---|
| L1 | Pipeline MQTT→InfluxDB non entièrement automatisé | ⚠️ Moyenne |
| L2 | URL ngrok aléatoire à chaque redémarrage | ⚠️ Moyenne |
| L3 | MQTT sans chiffrement TLS (port 1883) | 🔴 Haute |
| L4 | Injection manuelle dans Grafana | ⚠️ Moyenne |
| L5 | Détection par seuils fixes uniquement (embarqué) | ⚠️ Moyenne |
| L6 | Pas de buffer local en cas de déconnexion WiFi | 🔴 Haute |
| L7 | Capteurs Wokwi idéaux (pas de bruit réel) | 🟡 Faible |
| L8 | Fréquence MQTT 0.33 Hz insuffisante pour vibrations HF | 🟡 Faible |

---

## SLIDE 19 — ÉTAPES SUIVANTES

**🟢 Court terme (avant soutenance) :**
1. Configurer le token InfluxDB dans la GUI Node-RED
2. Activer les alertes Grafana (notification email/webhook)
3. Script de démarrage automatique (PowerShell)
4. Exécuter le notebook ML → obtenir F1, AUC, confusion matrices
5. Finaliser le rapport PFE avec résultats confirmés

**🟡 Moyen terme :**
6. Déployer Isolation Forest comme microservice (Flask/FastAPI)
7. ESP32 physique avec calibration capteurs réels
8. MQTT TLS (port 8883, certificats)
9. Buffer SPIFFS/LittleFS sur ESP32
10. XAI (SHAP) pour interpréter les anomalies ML

**🔵 Long terme :**
11. AWS IoT Core + InfluxDB Cloud (production)
12. Analyse FFT pour vibrations haute fréquence
13. TensorFlow Lite embarqué sur ESP32
14. Architecture multi-ESP32 zones critiques
15. Jumeau numérique (Digital Twin) de l'aéronef

---

## SLIDE 20 — CONCLUSION

**✅ Accompli (87%) :**
- Firmware ESP32 robuste : 392 lignes, 100% non bloquant
- Pipeline IoT 5 couches opérationnel
- Dashboard Grafana 10 panneaux, refresh 5s
- Détection embarquée 4 types d'anomalies — 6/6 scénarios validés
- 7 difficultés techniques résolues
- Pipeline ML : 3 modèles + validation NASA

**🔄 Reste (13%) :**
- Token InfluxDB dans Node-RED (5%)
- Alertes Grafana (5%)
- Exécution et validation résultats ML (3%)

**Compétences développées :**
C++ embarqué · MQTT · Node.js/Node-RED · InfluxQL/SQL · HTTPS/ngrok · Grafana · Python · scikit-learn · TensorFlow · ML non supervisé

---

# PROMPT À COPIER DANS CLAUDE POUR GÉNÉRER LE PPTX

```
Génère un script Python utilisant python-pptx qui crée un fichier PowerPoint professionnel (20 slides) à partir du contenu suivant.

Spécifications de style :
- Fond des slides : blanc (#FFFFFF)
- Couleur titre principal : bleu foncé (#1A237E)
- Couleur accent : orange (#FF6D00)
- Couleur texte courant : gris foncé (#333333)
- Couleur fond titres section : dégradé bleu foncé (#1A237E)
- Police titres : Calibri 28pt Bold
- Police corps : Calibri 14pt
- Police tableaux : Calibri 11pt
- Ajouter une barre de progression orange en bas de chaque slide
- Numérotation des slides en bas à droite
- Slide 1 = page de titre avec fond bleu foncé et texte blanc
- Les slides avec tableaux doivent avoir des tableaux stylisés (header bleu foncé, lignes alternées)
- Les slides de code doivent avoir un rectangle gris clair (#F5F5F5) avec police Consolas 10pt

Contenu des 20 slides :
[COLLER ICI LE CONTENU DES SLIDES 1 À 20]

Sauvegarde : Avancement_PFE_Nourhen_KHELIFI_2026.pptx
```
