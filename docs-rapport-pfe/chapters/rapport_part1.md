# Rapport Technique de Stage
## Solution Embarquee IoT - Monitoring Aeronautique

**Auteure :** Nourhen KHELIFI | **Reference :** CDC_2026_NourhenKHELIFI_YC_ES20268812
**Date :** 6 aout 2026 | **Version :** 1.0

---

## 1. Introduction

Le secteur aeronautique exige la surveillance continue des parametres critiques. Ce projet realise un pipeline IoT complet : ESP32 -> MQTT -> Node-RED -> InfluxDB -> Grafana, avec detection embarquee d'anomalies.

Plateforme de developpement : Windows 10 v26200.8875. Simulation via Wokwi (pas de materiel physique). Services cloud : HiveMQ Public, Grafana Cloud (gratuit), InfluxDB 3 Core (open source).

---

## 2. Architecture Generale - Pipeline 5 Couches

`
COUCHE 5 : VISUALISATION
  Grafana Cloud (prudentteal1570.grafana.net)
  Dashboard 10 panels, refresh 5s, InfluxQL
          |
          | HTTPS via ngrok (chimp-cryptic-possible.ngrok-free.dev)
          |
COUCHE 4 : STOCKAGE
  InfluxDB 3 Core v3.11.0 (localhost:8181)
  Database: aircraft | Measurement: sensors
  Champs: temperature, humidity, pressure, altitude, accX, accY, accZ, potentiometer
          |
          | HTTP API / Line Protocol v2
          |
COUCHE 3 : MIDDLEWARE
  Node-RED (localhost:1880)
  Flow: mqtt in -> parse JSON -> format InfluxDB -> write
          |
          | MQTT TCP/IP - Topic: aircraft/sensors
          |
COUCHE 2 : BROKER MQTT
  HiveMQ Public (broker.hivemq.com:1883)
  ESP32: AircraftESP32-[MAC] | Node-RED: nodered-aircraft
          |
          | WiFi IEEE 802.11 b/g/n (SSID: Wokwi-GUEST)
          |
COUCHE 1 : ACQUISITION
  ESP32 DevKit C v4 (simule via Wokwi)
  DHT22 GPIO15 | BMP180 I2C | MPU6050 I2C
  LCD 20x4 | Potentiometre GPIO34 | Bouton GPIO13
  LED Verte GPIO26 | LED Rouge GPIO27 | Buzzer GPIO25
`

---

## 3. Exigences du Projet (CDC)

| ID | Exigence fonctionnelle |
|---|---|
| EF-01 | Acquisition temperature/humidite via DHT22 |
| EF-02 | Mesure pression/altitude via BMP180 |
| EF-03 | Capture acceleration X/Y/Z via MPU6050 |
| EF-04 | Lecture signal analogique (potentiometre 0-4095) |
| EF-05 | Lectures non bloquantes (1 Hz capteurs, 0.33 Hz MQTT) |
| EF-06 | Transmission MQTT JSON vers HiveMQ |
| EF-07 | Detection anomalies embarquee (LED + buzzer) |
| EF-08 | Affichage LCD 20x4 temps reel |
| EF-09 | Stockage InfluxDB (serie temporelle) |
| EF-10 | Dashboard Grafana (graphiques, jauges, stats) |

| ID | Exigence technique |
|---|---|
| ET-01 | ESP32 DevKit C v4 (240 MHz dual-core, 520 KB RAM) |
| ET-02 | MQTT v3.1.1, port 1883, QoS 0 |
| ET-03 | JSON: timestamp, temperature, humidity, pressure, altitude, accX, accY, accZ, potentiometer, status, reason |
| ET-04 | InfluxDB 3 Core v3.11.0, bucket "aircraft", measurement "sensors" |
| ET-05 | Grafana Cloud 13.2.0, datasource InfluxQL |
| ET-06 | Node-RED local, noeuds mqtt in + function + influxdb out |
| ET-07 | Simulation Wokwi sans materiel physique |

---

## 4. Choix Technologiques - Comparaisons

### ESP32 vs Alternatives

| Critere | ESP32 | Arduino Uno | RPi Zero | STM32 |
|---|---|---|---|---|
| WiFi integre | OUI | NON | OUI | NON |
| Dual core 240MHz | OUI | NON (16MHz) | OUI (1GHz) | Partiel |
| RAM | 520 KB | 2 KB | 512 MB | 64-512 KB |
| Prix | ~5 EUR | ~20 EUR | ~15 EUR | ~5-20 EUR |
| Wokwi natif | OUI | Partiel | NON | Partiel |

### MQTT vs Alternatives

| Critere | MQTT | HTTP REST | WebSocket | CoAP |
|---|---|---|---|---|
| Overhead | 2 octets en-tete | Eleve (headers) | Moyen | Faible |
| Modele | Pub/Sub | Req/Resp | Bidirectionnel | Req/Resp |
| Reconnexion auto | OUI (QoS) | Manuelle | Manuelle | Non |
| IoT standard | IEEE/OASIS | IETF | IETF | IETF |

### InfluxDB vs Alternatives

| Critere | InfluxDB 3 | TimescaleDB | Prometheus | SQLite |
|---|---|---|---|---|
| Serie temporelle natif | OUI | OUI (ext) | OUI | NON |
| SQL + InfluxQL | OUI | SQL seul | PromQL | SQL |
| Grafana officiel | OUI | OUI | OUI | Limite |
| Parquet interne | OUI | NON | NON | NON |
| Cout | Gratuit | Gratuit+ | Gratuit | Gratuit |

### Grafana vs Alternatives

| Critere | Grafana | Kibana | Tableau | Power BI |
|---|---|---|---|---|
| IoT/TSDB | OUI | Partiel | NON | Partiel |
| InfluxDB natif | OUI | NON | NON | NON |
| Refresh temps reel | OUI | OUI | Limite | Limite |
| Cloud gratuit | OUI | NON | Payant | Payant/O365 |

### Wokwi vs Alternatives

| Critere | Wokwi | Proteus | SimulIDE | TinkerCAD |
|---|---|---|---|---|
| ESP32 complet | OUI | Limite | Limite | Partiel |
| WiFi + MQTT | OUI | NON | NON | NON |
| Extension VS Code | OUI | NON | NON | NON |

---

## 5. Firmware ESP32 - sketch.ino (392 lignes)

### 5.1 Structure modulaire

`
sketch.ino
+-- Includes: Wire, WiFi, PubSubClient, DHT, BMP085, MPU6050, LCD, time
+-- Constantes PIN: DHTPIN=15, POT_PIN=34, BUTTON_PIN=13
                     GREEN_LED=26, RED_LED=27, BUZZER_PIN=25
+-- Timers non bloquants:
    READ_INTERVAL=1000ms, SERIAL_INTERVAL=2000ms
    LCD_INTERVAL=1000ms, MQTT_INTERVAL=3000ms
    BUTTON_DEBOUNCE_MS=200ms, RECONNECT_INTERVAL=5000ms
+-- Filtre: FILTER_SIZE=5, tempBuffer[5]
+-- Fonctions: movingAverage, getTimestamp, setup_wifi, setup_time
               readSensors, detectAnomaly, displayLCD, sendMQTT
               reconnectMQTT_nonBlocking, checkButton
+-- setup() + loop() 100% non bloquant
`

### 5.2 Ordre initialisation setup()

1. Serial.begin(115200) + delay(1000)
2. Wire.begin(21, 22) -- I2C SDA/SCL
3. pinMode LEDs/BUTTON/BUZZER
4. tempBuffer[] rempli avec zeros
5. lcd.init() + lcd.backlight() + "Init..."
6. dht.begin()
7. bmp.begin() avec verification
8. mpu.begin() avec verification
9. setup_wifi() -- timeout 20 x 500ms = 10s
10. setup_time() -- NTP pool.ntp.org, timeout 4.5s
11. snprintf(mqttClientId, "AircraftESP32-%s", WiFi.macAddress())
12. client.setServer() + client.setBufferSize(512)
13. reconnectMQTT_nonBlocking()

### 5.3 Boucle loop() - Pattern non bloquant

`cpp
void loop() {
    unsigned long now = millis();
    checkButton();
    if (now - lastReadTime >= 1000) { readSensors(); detectAnomaly(); }
    if (now - lastLCDTime >= 1000) { displayLCD(); }
    if (now - lastSerialTime >= 2000) { printDebugInfo(); }
    reconnectMQTT_nonBlocking();
    if (client.connected()) client.loop();
    if (now - lastMQTTTime >= 3000) { sendMQTT(); }
}
`

**Zero delay() dans loop()** : Sur ESP32, Serial est toujours pret. while(!Serial){delay(10)} provoque une boucle infinie gelee dans Wokwi. Supprime.

### 5.4 Format JSON MQTT publie

`json
{
  "timestamp": 1754481840,
  "temperature": 24.50,
  "humidity": 55.20,
  "pressure": 1013.25,
  "altitude": 45.00,
  "accX": 0.12,
  "accY": -0.05,
  "accZ": 9.81,
  "potentiometer": 45,
  "status": "NORMAL",
  "reason": ""
}
`

Taille ~300 octets -> client.setBufferSize(512) obligatoire (defaut 256 insuffisant).

---

## 6. Capteurs - Configuration Detaillee

### DHT22 (Temperature + Humidite)
- GPIO15, one-wire numerique, 1 Hz
- Plage: -40 a +80 degC (+/-0.5), 0-100% RH (+/-2-5%)
- Gestion erreur: !isnan() avant utilisation
- Filtrage temperature: moyenne glissante 5 echantillons
  [24.1, 24.3, 23.9, 24.5, 24.2] -> 24.2 degC

### BMP180 (Pression + Altitude)
- I2C adresse 0x77, GPIO21/22, 1 Hz
- Pression: bmp.readPressure()/100.0 (Pa -> hPa)
- Altitude: bmp.readAltitude() (ref 1013.25 hPa)
- Bug corrige: 47750 Pa (impossible) -> 101325 Pa dans diagram.json

### MPU6050 (Accelerometre)
- I2C adresse 0x68, GPIO21/22, 1 Hz
- accX, accY, accZ en m/s2 (accZ ~9.81 en repos = gravite)
- Gyroscope non exploite dans cette version

### Potentiometre
- GPIO34 analogique, ADC 12 bits (0-4095)
- map(analogRead(), 0, 4095, 0, 100) -> pourcentage
- Double role: mesure + generateur de defauts (>50%)

---

## 7. Simulation de Defauts (Potentiometre)

`
Pot < 50%: Fonctionnement normal
Pot > 50%: factor = (pot-50)/50.0 [0.0 a 1.0]
    temperature += 25.0 * factor   (+0 a +25 degC)
    pressure    -= 250.0 * factor   (-0 a -250 hPa)
    altitude    += 1500.0 * factor  (+0 a +1500 m)
    accX,Y,Z   += 20.0 * factor    (+0 a +20 m/s2)
Pot > 80%: ALERT "ENGINE FAILURE" systematique
`

---

## 8. Detection des Anomalies

`
Priorite 1: temperature > 45 degC     -> ALERT: HIGH TEMP
Priorite 2: pressure < 850 hPa (>0)   -> ALERT: LOW PRESSURE
Priorite 3: vibration > 15 m/s2        -> ALERT: HIGH VIBRATION
    vibration = sqrt(accX^2 + accY^2 + (accZ-9.8)^2)
    (gravite soustraite pour mesurer vibration pure)
Priorite 4: pot > 80%                  -> ALERT: ENGINE FAILURE
`

Actions en mode ALERT:
- LED Verte (GPIO26): eteinte
- LED Rouge (GPIO27): allumee
- Buzzer (GPIO25): tone(1500 Hz)
- LCD ligne 4: raison anomalie
- MQTT: status="ALERT", reason="[raison]"

Limites: seuils fixes, pas de correlation multi-parametrique, pas d'apprentissage.

---

## 9. Configuration Node-RED

### Noeud fn_parse_validate
`javascript
if (typeof raw === 'object') { /* passage direct */ }
if (raw.trim().length === 0) { node.warn(...); return null; }
try { data = JSON.parse(raw); }
catch(e) { node.error(...); return null; }
if (!data.timestamp) data.timestamp = Math.floor(Date.now()/1000);
`

### Noeud fn_to_influx_points
`javascript
msg.payload = [{
    measurement: "sensors",
    fields: {
        temperature: Number(d.temperature),
        humidity: Number(d.humidity),
        pressure: Number(d.pressure),
        altitude: Number(d.altitude),
        accX: Number(d.accX),
        accY: Number(d.accY),
        accZ: Number(d.accZ),
        potentiometer: Number(d.potentiometer)
    },
    tags: { device: "ESP32" },
    timestamp: Date.now()
}];
`

### Config InfluxDB Node-RED
- Plugin: node-red-contrib-influxdb v0.7.0
- URL: http://127.0.0.1:8181
- Bucket: aircraft | Org: aircraft_org | Precision: ms

### Config HiveMQ Node-RED
- broker.hivemq.com:1883 | MQTT v3.1.1
- Client: nodered-aircraft | Keep-alive: 60s

---

## 10. Schema InfluxDB 3 Core

| Colonne | Type | Description |
|---|---|---|
| time | Timestamp(ns) | Horodatage auto InfluxDB |
| device | Utf8 (tag, indexe) | "ESP32" |
| temperature | Float64 | degC |
| humidity | Float64 | % |
| pressure | Float64 | hPa |
| altitude | Float64 | m |
| accX | Float64 | m/s2 |
| accY | Float64 | m/s2 |
| accZ | Float64 | m/s2 |
| potentiometer | Float64 | % (0-100) |

Endpoints utilises:
- POST /api/v2/write?bucket=aircraft&precision=ns (ecriture)
- POST /api/v3/query_sql (requetes SQL)
- GET /query?db=aircraft&q=... (InfluxQL, utilise par Grafana)

---

## 11. Dashboard Grafana - 10 Panels

URL: https://prudentteal1570.grafana.net/d/atdh9j/aircraft-esp32-sensor-dashboard
UID: atdh9j | Refresh: 5s | Plage: derniere heure

| Panel | Type | Donnee | Position |
|---|---|---|---|
| Temperature (degC) | Time series | mean(temperature) | x0,y0,w12,h8 |
| Humidity (%) | Time series | mean(humidity) | x12,y0,w12,h8 |
| Pressure (hPa) | Time series | mean(pressure) | x0,y8,w12,h8 |
| Altitude (m) | Time series | mean(altitude) | x12,y8,w12,h8 |
| Accel X/Y/Z | Time series | mean(accX/Y/Z) | x0,y16,w16,h8 |
| Potentiometre | Gauge | last(potentiometer) | x16,y16,w8,h8 |
| Temp Now | Stat | last(temperature) | x0,y24,w6,h4 |
| Humidity Now | Stat | last(humidity) | x6,y24,w6,h4 |
| Pressure Now | Stat | last(pressure) | x12,y24,w6,h4 |
| Altitude Now | Stat | last(altitude) | x18,y24,w6,h4 |

Requetes InfluxQL (mode choisi apres echec gRPC avec ngrok) :
`sql
SELECT mean("temperature") FROM "sensors" WHERE 
GROUP BY time() fill(null)
`

fill(null): lacunes plutot qu'interpolation. mean(): agregation sur intervalles Grafana.

---

## 12. Difficultes Rencontrees et Solutions

### D1: Erreur "Unexpected end of JSON input" Node-RED
- Cause: Messages MQTT vides (retained/LWT) + topics desynchronises
- Solution: Validation JS robuste avec gestion explicite cas vide/invalide
- Statut: Resolu

### D2: Simulation Wokwi gelee
- Cause: while(!Serial){delay(10);} en loop() -> boucle infinie sur ESP32
- Solution: Suppression complete du pattern
- Statut: Resolu

### D3: Pression BMP180 impossible (47750 Pa)
- Cause: Valeur par defaut incorrecte dans diagram.json
- Impact: Altitude ~5800m, fausse alarme LOW PRESSURE au demarrage
- Solution: Correction a 101325 Pa dans diagram.json
- Statut: Resolu

### D4: Incompatibilite InfluxDB 3 gRPC / ngrok (CRITIQUE)
- Cause: InfluxDB 3 SQL = gRPC/HTTP2. ngrok free ne supporte pas HTTP2 FlightSQL.
- Erreur: "transport: received EOF, want RST_STREAM or HEADERS"
- Solution: Passage mode InfluxQL (endpoint /query, HTTP/1.1) dans Grafana
- Validation: "datasource is working. 1 measurements found"
- Statut: Resolu

### D5: Token InfluxDB non configure dans Node-RED
- Cause: Credentials chiffres dans flows_cred.json, injection programmatique echouee
- Impact: 401 Unauthorized sur chaque tentative d'ecriture depuis Node-RED
- Solution contournement: Injection directe via API /api/v2/write
- Statut: Partiellement resolu (a finaliser via GUI Node-RED)

### D6: Version ngrok obsolete (3.3.1)
- Cause: Paquet winget pointe vers version ancienne
- Erreur: ERR_NGROK_121 (minimum 3.20.0 requis)
- Solution: ngrok update -> 3.39.10
- Statut: Resolu

### D7: Client MQTT duplique sur broker public
- Cause: Client ID statique -> deconnexion immediate si double instance
- Solution: ID = "AircraftESP32-[MAC]" (unicite par adresse MAC)
- Statut: Resolu

---

## 13. Tests et Resultats

### Tests firmware (tous OK)

| Fonction | Test | Resultat |
|---|---|---|
| movingAverage() | Buffer 5 valeurs | Correct |
| getTimestamp() | NTP sync | epoch > 1700000000 |
| readSensors() | Valeurs dans plages | OK |
| detectAnomaly() | 5 scenarios seuils | Tous conformes |
| sendMQTT() | Payload 300+ octets | Publie |
| reconnectMQTT() | Sans blocage | OK |

### Tests API InfluxDB (tous OK)

| Test | Endpoint | Statut |
|---|---|---|
| Health local | GET /ping | 200 OK |
| Auth Bearer | Authorization: Bearer | 200 OK |
| SQL | POST /api/v3/query_sql | Donnees retournees |
| InfluxQL | GET /query | Donnees retournees |
| Ecriture | POST /api/v2/write | 204 No Content |

### Tests ngrok (tous OK)

| Test | Resultat |
|---|---|
| GET /ping via ngrok | 200 OK |
| SQL via ngrok | [{"Int64(1)":1}] |
| InfluxQL via ngrok | {results:[{series:[...]}]} |

### Test Grafana datasource
Resultat: "datasource is working. 1 measurements found" (STATUS: OK)

### Scenarios anomalies valides

| Scenario | Condition | Attendu | Resultat |
|---|---|---|---|
| Normal | Pot 0% | NORMAL | Conforme |
| Haute temp | Pot 95% -> 47.5 degC | ALERT HIGH TEMP | Conforme |
| Basse pression | Pot 85% -> 838 hPa | ALERT LOW PRESSURE | Conforme |
| Vibration | Pot 80% -> 17 m/s2 | ALERT HIGH VIBRATION | Conforme |
| Panne moteur | Pot 90% | ALERT ENGINE FAILURE | Conforme |

---

## 14. Avancement Global

| Module | Etat | % | Justification |
|---|---|---|---|
| Architecture generale | Termine | 100% | Pipeline 5 couches defini et valide |
| Simulation Wokwi | Termine | 100% | Circuit complet, operationnel |
| Firmware ESP32 | Termine | 100% | Compile 974KB, tous scenarios OK |
| Filtrage/pretraitement | Termine | 100% | Filtre, NTP, deduplication LCD |
| Communication MQTT | Termine | 100% | Topic, JSON, reconnexion QoS |
| Broker HiveMQ | Termine | 100% | Connexions ESP32+Node-RED stables |
| Node-RED flux | Quasi-termine | 95% | 5% = token InfluxDB via GUI |
| InfluxDB structure | Quasi-termine | 95% | 5% = pipeline MQTT->InfluxDB auto |
| Dashboard Grafana | Quasi-termine | 95% | 5% = alertes Grafana |
| Tunnel ngrok | Termine | 100% | Valide end-to-end |
| Detection anomalies embarquee | Termine | 85% | 15% = ML non implemente |
| Detection anomalies serveur | En cours | 30% | ML non developpe |
| Tests validation | En cours | 80% | Performance non testee |
| Documentation | En cours | 75% | Rapport en cours |

**AVANCEMENT GLOBAL : 87%**

---

## 15. Limites et Ameliorations

### Limites actuelles
- L1: Pipeline MQTT->InfluxDB non entierement automatise (token Node-RED)
- L2: ngrok URL aleatoire a chaque redemarrage (pas de production)
- L3: MQTT sans chiffrement TLS (port 1883)
- L4: Donnees Grafana actuelles = injection manuelle, pas temps reel complet
- L5: Detection par seuils fixes (pas d'apprentissage automatique)
- L6: Pas de buffer local si perte connexion (donnees perdues)
- L7: Capteurs Wokwi ideaux (pas de bruit, pas de derive)
- L8: 0.33 Hz MQTT insuffisant pour vibrations haute frequence

### Ameliorations court terme (avant soutenance)
1. Token InfluxDB dans GUI Node-RED
2. Alertes Grafana (email/webhook)
3. Script PowerShell demarrage automatique
4. Tests performance (latence bout-en-bout)

### Ameliorations moyen terme
5. ML cote serveur: Isolation Forest (scikit-learn) sur donnees InfluxDB
6. Deploiement physique ESP32 avec calibration capteurs
7. MQTT TLS port 8883 avec certificats
8. Buffer SPIFFS/LittleFS sur ESP32

### Ameliorations long terme
9. Deploiement cloud complet (AWS IoT Core + InfluxDB Cloud)
10. Dashboard FFT, cartes geographiques, rapports PDF
11. TensorFlow Lite embarque pour detection sans cloud
12. Architecture multi-ESP32 zones critiques

---

## 16. Conclusion

Ce rapport presente l'avancement a 87% d'un projet IoT aeronautique academique.

Realisations principales:
- Firmware ESP32 robuste 392 lignes, 100% non bloquant, 974 KB compile
- Pipeline 5 couches: Wokwi -> HiveMQ -> Node-RED -> InfluxDB -> Grafana
- Dashboard Grafana 10 panels operationnel avec health check valide
- Detection embarquee 4 types anomalies, tous scenarios testes
- 7 difficultes techniques resolues dont incompatibilite gRPC/ngrok

Restant: finalisation token Node-RED, alertes Grafana, detection ML serveur.

Competences developpees: C++ embarque, MQTT, Node.js, SQL/InfluxQL, HTTPS/ngrok, Grafana API.

---
*Nourhen KHELIFI | CDC_2026_NourhenKHELIFI_YC_ES20268812 | 6 aout 2026*