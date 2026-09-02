# Diagrammes UML — Projet PFE IoT Aéronautique
## Nourhen KHELIFI — YaneCode Digital — Été 2026

> Tous les diagrammes ci-dessous sont adaptés à l'architecture réelle du projet :
> **ESP32 (Wokwi) → MQTT (HiveMQ) → Node-RED → InfluxDB 3 Core → Grafana Cloud**

---

## 1. Diagramme de cas d'utilisation

```plantuml
@startuml
left to right direction
skinparam actorStyle awesome

actor "Opérateur\nde maintenance" as User
actor "ESP32\n(Système embarqué)" as ESP32

rectangle "Solution IoT — Monitoring Aéronautique" {

  package "Supervision" {
    usecase "Consulter le Dashboard Grafana" as UC1
    usecase "Visualiser les mesures\nen temps réel" as UC2
    usecase "Consulter l'historique\ndes mesures" as UC3
    usecase "Visualiser les graphiques\n(température, pression, vibration)" as UC6
    usecase "Consulter les statistiques\n(min, max, mean)" as UC7
  }

  package "Alertes et Anomalies" {
    usecase "Recevoir une alerte\n(LED, Buzzer, LCD)" as UC9
    usecase "Détecter une anomalie\n(seuils embarqués)" as UC8_emb
    usecase "Détecter une anomalie\n(ML serveur : Isolation Forest)" as UC8_ml
    usecase "Consulter le Risk Score" as UC12
  }

  package "Données" {
    usecase "Acquérir les données\ncapteurs (DHT22, BMP180, MPU6050)" as UC_acq
    usecase "Transmettre les données\nvia MQTT" as UC_mqtt
    usecase "Stocker les données\ndans InfluxDB" as UC_store
    usecase "Actualiser les données\n(refresh 5s)" as UC11
  }
}

User --> UC1
User --> UC2
User --> UC3
User --> UC6
User --> UC7
User --> UC9
User --> UC12

ESP32 --> UC_acq
ESP32 --> UC8_emb
ESP32 --> UC_mqtt
ESP32 --> UC9

UC2 ..> UC11 : <<include>>
UC3 ..> UC11 : <<include>>
UC6 ..> UC11 : <<include>>
UC7 ..> UC11 : <<include>>
UC_mqtt ..> UC_store : <<include>>
UC8_emb ..> UC9 : <<extend>>
UC8_ml ..> UC12 : <<extend>>
UC_acq ..> UC_mqtt : <<include>>

@enduml
```

---

## 2. Diagramme de classes

```plantuml
@startuml
skinparam classAttributeIconSize 0

class Operateur {
  - id : int
  - nom : String
  - role : String
  + consulterDashboard()
  + consulterHistorique()
  + consulterAlertes()
}

class ESP32 {
  - macAddress : String
  - ssid : String = "Wokwi-GUEST"
  - mqttClientId : String
  - readInterval : int = 1000
  - mqttInterval : int = 3000
  - filterSize : int = 5
  + setup()
  + loop()
  + readSensors()
  + detectAnomaly()
  + sendMQTT()
  + displayLCD()
  + reconnectMQTT_nonBlocking()
}

class DHT22 {
  - pin : int = 15
  - type : String = "DHT22"
  + readTemperature() : float
  + readHumidity() : float
}

class BMP180 {
  - i2cAddress : int = 0x77
  - referencePressure : float = 1013.25
  + readPressure() : float
  + readAltitude() : float
}

class MPU6050 {
  - i2cAddress : int = 0x68
  + getAcceleration() : SensorEvent
}

class Potentiometre {
  - pin : int = 34
  - resolution : int = 12
  + readPercent() : int
}

class MoyenneGlissante {
  - bufferSize : int = 5
  - tempBuffer : float[]
  - bufferIndex : int
  + movingAverage(buffer : float[]) : float
}

class MesureJSON {
  - timestamp : long
  - temperature : float
  - humidity : float
  - pressure : float
  - altitude : float
  - accX : float
  - accY : float
  - accZ : float
  - potentiometer : int
  - status : String
  - reason : String
  + toJSON() : String
}

class DetectionSeuilsEmbarquee {
  - seuilTemperature : float = 45.0
  - seuilPression : float = 850.0
  - seuilVibration : float = 15.0
  - seuilPotentiometre : int = 80
  + detectAnomaly(mesure : MesureJSON) : String
  + calculerVibration(ax : float, ay : float, az : float) : float
}

class AlerteLocale {
  - ledVerte : int = 26
  - ledRouge : int = 27
  - buzzer : int = 25
  - lcd : LiquidCrystal_I2C
  + activerAlerte(reason : String)
  + desactiverAlerte()
  + afficherLCD(mesure : MesureJSON)
}

class MQTTClient {
  - broker : String = "broker.hivemq.com"
  - port : int = 1883
  - topic : String = "aircraft/sensors"
  - qos : int = 0
  - bufferSize : int = 512
  + connect()
  + publish(topic : String, payload : String)
  + reconnectNonBlocking()
}

class NodeRED {
  - flowId : String = "flow_aircraft"
  + parseValidateJSON(payload : String) : Object
  + formatInfluxPoints(data : Object) : Object
  + routeToInfluxDB(points : Object)
}

class InfluxDB {
  - url : String = "http://127.0.0.1:8181"
  - bucket : String = "aircraft"
  - measurement : String = "sensors"
  - org : String = "aircraft_org"
  + writePoint(point : Object)
  + querySQL(query : String) : ResultSet
  + queryInfluxQL(query : String) : ResultSet
}

class GrafanaDashboard {
  - url : String
  - uid : String = "atdh9j"
  - refreshInterval : int = 5
  - panels : int = 10
  + afficherTemperature()
  + afficherPression()
  + afficherHumidite()
  + afficherAltitude()
  + afficherAcceleration()
  + afficherPotentiometre()
  + afficherStatistiques()
}

class IsolationForest {
  - nEstimators : int = 200
  - contamination : float = 0.05
  - features : String[]
  + fit(X_train : float[][])
  + predict(X : float[][]) : int[]
  + scoreSamples(X : float[][]) : float[]
}

class HiveMQBroker {
  - host : String = "broker.hivemq.com"
  - port : int = 1883
  - protocol : String = "MQTT v3.1.1"
  + receiveMessage(topic : String) : String
  + distributeMessage(topic : String, payload : String)
}

' ── Relations ──
ESP32 "1" *-- "1" DHT22 : contient
ESP32 "1" *-- "1" BMP180 : contient
ESP32 "1" *-- "1" MPU6050 : contient
ESP32 "1" *-- "1" Potentiometre : contient
ESP32 "1" *-- "1" MoyenneGlissante : utilise
ESP32 "1" *-- "1" DetectionSeuilsEmbarquee : utilise
ESP32 "1" *-- "1" AlerteLocale : déclenche
ESP32 "1" *-- "1" MQTTClient : publie via

ESP32 "1" --> "0..*" MesureJSON : génère

MQTTClient "1" --> "1" HiveMQBroker : publie vers
HiveMQBroker "1" --> "1" NodeRED : distribue à
NodeRED "1" --> "1" InfluxDB : écrit dans
InfluxDB "1" --> "1" GrafanaDashboard : alimente
InfluxDB "1" --> "0..*" MesureJSON : stocke

DetectionSeuilsEmbarquee "1" --> "0..*" AlerteLocale : déclenche
IsolationForest "1" --> "0..*" MesureJSON : analyse

Operateur "1" --> "1" GrafanaDashboard : consulte

@enduml
```

---

## 3. Diagramme de séquence — Consultation du Dashboard

```plantuml
@startuml
skinparam sequenceArrowThickness 2

actor "Opérateur" as User
participant "Grafana Cloud" as Grafana
participant "InfluxDB 3 Core" as InfluxDB
participant "Node-RED" as NodeRED
participant "HiveMQ Broker" as MQTT
participant "ESP32 (Wokwi)" as ESP32

User -> Grafana : consulterDashboard()
activate Grafana

Grafana -> InfluxDB : queryInfluxQL(\n"SELECT mean(temperature)\n FROM sensors\n WHERE time > now()-1h\n GROUP BY time()")
activate InfluxDB
InfluxDB --> Grafana : sensorData (séries temporelles)
deactivate InfluxDB

Grafana -> Grafana : renderPanels()\n[10 panels : temp, hum,\npression, alt, acc, pot,\n4 stats]

Grafana --> User : dashboardAffiché\n(refresh auto 5s)
deactivate Grafana

@enduml
```

---

## 4. Diagramme de séquence — Acquisition et transmission en temps réel

```plantuml
@startuml
skinparam sequenceArrowThickness 2

actor "Opérateur" as User
participant "ESP32 (Wokwi)" as ESP32
participant "DHT22" as DHT
participant "BMP180" as BMP
participant "MPU6050" as MPU
participant "Potentiomètre" as POT
participant "Filtre\nMoyenne Glissante" as Filter
participant "Détection\nSeuils" as Detect
participant "Alerte Locale\n(LED/Buzzer/LCD)" as Alert
participant "HiveMQ\nBroker" as MQTT
participant "Node-RED" as NodeRED
participant "InfluxDB" as InfluxDB
participant "Grafana" as Grafana

loop Toutes les 1000 ms (READ_INTERVAL)
  ESP32 -> DHT : readTemperature()
  activate DHT
  DHT --> ESP32 : temperature (°C)
  deactivate DHT

  ESP32 -> DHT : readHumidity()
  activate DHT
  DHT --> ESP32 : humidity (%)
  deactivate DHT

  ESP32 -> BMP : readPressure() / 100.0
  activate BMP
  BMP --> ESP32 : pressure (hPa)
  deactivate BMP

  ESP32 -> BMP : readAltitude()
  activate BMP
  BMP --> ESP32 : altitude (m)
  deactivate BMP

  ESP32 -> MPU : getEvent()
  activate MPU
  MPU --> ESP32 : accX, accY, accZ (m/s²)
  deactivate MPU

  ESP32 -> POT : analogRead() → map(0-4095, 0-100)
  activate POT
  POT --> ESP32 : potPercent (%)
  deactivate POT

  ESP32 -> Filter : movingAverage(tempBuffer[5])
  activate Filter
  Filter --> ESP32 : temperatureFiltrée
  deactivate Filter

  alt potPercent > 50 (Simulation de défaut)
    ESP32 -> ESP32 : factor = (pot-50)/50.0\ntemp += 25*factor\npressure -= 250*factor\naltitude += 1500*factor\nacc += 20*factor
  end

  ESP32 -> Detect : detectAnomaly(mesures)
  activate Detect

  alt temperature > 45°C
    Detect --> ESP32 : ALERT: HIGH TEMP
  else pressure < 850 hPa
    Detect --> ESP32 : ALERT: LOW PRESSURE
  else vibration > 15 m/s²
    Detect --> ESP32 : ALERT: HIGH VIBRATION
  else potPercent > 80%
    Detect --> ESP32 : ALERT: ENGINE FAILURE
  else Tout normal
    Detect --> ESP32 : NORMAL
  end
  deactivate Detect

  alt status == "ALERT"
    ESP32 -> Alert : activerAlerte(reason)
    activate Alert
    Alert -> Alert : LED rouge ON\nLED verte OFF\nBuzzer 1500 Hz\nLCD: reason
    Alert --> ESP32 : alerteActivée
    deactivate Alert
  else status == "NORMAL"
    ESP32 -> Alert : desactiverAlerte()
    activate Alert
    Alert -> Alert : LED verte ON\nLED rouge OFF\nBuzzer OFF
    Alert --> ESP32 : normal
    deactivate Alert
  end
end

loop Toutes les 3000 ms (MQTT_INTERVAL)
  ESP32 -> ESP32 : construirePayloadJSON()\n{"timestamp", "temperature",\n"humidity", "pressure",\n"altitude", "accX", "accY",\n"accZ", "potentiometer",\n"status", "reason"}

  ESP32 -> MQTT : publish("aircraft/sensors", payload)\n[~300 octets, QoS 0]
  activate MQTT
  MQTT --> ESP32 : publishOK
  deactivate MQTT

  MQTT -> NodeRED : subscribe("aircraft/sensors")
  activate NodeRED
  NodeRED -> NodeRED : fn_parse_validate()\n[vérif JSON vide/invalide]

  alt JSON valide
    NodeRED -> NodeRED : fn_to_influx_points()\n[measurement:"sensors",\ntags:{device:"ESP32"},\nfields:{temp,hum,press,...}]

    NodeRED -> InfluxDB : POST /api/v2/write\n?bucket=aircraft&precision=ms
    activate InfluxDB
    InfluxDB --> NodeRED : 204 No Content
    deactivate InfluxDB
  else JSON vide ou invalide
    NodeRED -> NodeRED : node.warn("Message\nMQTT vide, ignoré")
  end
  deactivate NodeRED
end

loop Toutes les 5s (Grafana refresh)
  Grafana -> InfluxDB : queryInfluxQL()
  activate InfluxDB
  InfluxDB --> Grafana : data
  deactivate InfluxDB
  Grafana --> User : dashboardMisÀJour
end

@enduml
```

---

## 5. Diagramme de séquence — Consultation de l'historique

```plantuml
@startuml
skinparam sequenceArrowThickness 2

actor "Opérateur" as User
participant "Grafana Cloud" as Grafana
participant "InfluxDB 3 Core" as InfluxDB

User -> Grafana : sélectionnerPériode(\nex: "Last 24 hours")
activate Grafana

Grafana -> InfluxDB : queryInfluxQL(\n"SELECT mean(temperature),\nmean(pressure),\nmean(humidity)\nFROM sensors\nWHERE time > now()-24h\nGROUP BY time(5m)\nfill(null)")
activate InfluxDB
InfluxDB --> Grafana : historicalData\n(séries temporelles horodatées)
deactivate InfluxDB

Grafana -> Grafana : renderTimeSeriesPanels()\n[Temperature, Pressure,\nHumidity, Altitude,\nAcceleration X/Y/Z]

Grafana -> Grafana : renderStatPanels()\n[Temp Now, Humidity Now,\nPressure Now, Altitude Now]

Grafana --> User : historiqueAffiché\n(courbes temporelles)
deactivate Grafana

@enduml
```

---

## 6. Diagramme de séquence — Détection d'anomalie complète (Embarqué + ML Serveur)

```plantuml
@startuml
skinparam sequenceArrowThickness 2

actor "Opérateur" as User
participant "ESP32 (Wokwi)" as ESP32
participant "Détection\nSeuils Embarquée" as DetectEmb
participant "Alerte Locale\n(LED/Buzzer/LCD)" as AlertLocal
participant "HiveMQ\nBroker" as MQTT
participant "Node-RED" as NodeRED
participant "InfluxDB" as InfluxDB
participant "Module ML\n(Isolation Forest)" as ML
participant "Grafana" as Grafana

== NIVEAU 1 — Détection Embarquée (< 1 ms) ==

ESP32 -> ESP32 : readSensors()
ESP32 -> DetectEmb : detectAnomaly(temperature=52°C,\npressure=780 hPa,\nvibration=18 m/s²)
activate DetectEmb

DetectEmb -> DetectEmb : vérifier seuils :\ntemp > 45 ? OUI → HIGH TEMP\npressure < 850 ? OUI → LOW PRESSURE\nvibration > 15 ? OUI → HIGH VIBRATION

DetectEmb --> ESP32 : status="ALERT",\nreason="HIGH TEMP"
deactivate DetectEmb

ESP32 -> AlertLocal : activerAlerte("HIGH TEMP")
activate AlertLocal
AlertLocal -> AlertLocal : LED rouge ON\nBuzzer 1500 Hz\nLCD: "HIGH TEMP"
AlertLocal --> ESP32 : alerteActivée
deactivate AlertLocal

ESP32 -> MQTT : publish("aircraft/sensors",\n{..., status:"ALERT",\nreason:"HIGH TEMP"})
activate MQTT

== NIVEAU 2 — Détection ML Serveur (~100 ms) ==

MQTT -> NodeRED : message reçu
activate NodeRED
NodeRED -> NodeRED : parseValidate(payload)
NodeRED -> InfluxDB : writePoint(sensors, fields)
activate InfluxDB
InfluxDB --> NodeRED : 204 OK
deactivate InfluxDB
deactivate NodeRED
deactivate MQTT

ML -> InfluxDB : querySQL(\n"SELECT * FROM sensors\nORDER BY time DESC\nLIMIT 20")
activate InfluxDB
InfluxDB --> ML : fenêtre 20 derniers messages
deactivate InfluxDB

activate ML
ML -> ML : scaler.transform(features)\n[22 features dont vibration_rms,\ntemp_gradient, battery_drain_rate,\npressure_hpa, ...]

ML -> ML : IsolationForest.predict(X_scaled)\n[n_estimators=200,\ncontamination=0.05]

ML -> ML : score = -score_samples(X)\n[plus le score est élevé,\nplus l'anomalie est probable]

alt score > seuil (anomalie ML détectée)
  ML -> Grafana : alerteGrafana(\n"Anomalie ML détectée\nscore=0.87")
  activate Grafana
  Grafana --> User : notification alerte
  deactivate Grafana
end
deactivate ML

@enduml
```

---

## 7. Diagramme de séquence — Simulation de défaut via potentiomètre

```plantuml
@startuml
skinparam sequenceArrowThickness 2

actor "Opérateur" as User
participant "Potentiomètre\n(GPIO34)" as POT
participant "ESP32" as ESP32
participant "Capteurs\n(DHT22/BMP180/MPU6050)" as Sensors
participant "Détection Seuils" as Detect
participant "Alerte Locale" as Alert
participant "MQTT → InfluxDB\n→ Grafana" as Pipeline

== Scénario Nominal (Pot = 0%) ==

User -> POT : positionner à 0%
POT --> ESP32 : potPercent = 0
ESP32 -> Sensors : readSensors()
Sensors --> ESP32 : temp=24.5, press=1013, vib=0.2
ESP32 -> Detect : detectAnomaly()
Detect --> ESP32 : status = "NORMAL"
ESP32 -> Alert : LED verte ON
ESP32 -> Pipeline : publish(status="NORMAL")

== Scénario Limite (Pot = 70%) ==

User -> POT : tourner à 70%
POT --> ESP32 : potPercent = 70
ESP32 -> ESP32 : factor = (70-50)/50 = 0.4\ntemp += 25×0.4 = +10°C → 34.5°C\npress -= 250×0.4 = -100 → 913 hPa\nalt += 1500×0.4 = +600m\nacc += 20×0.4 = +8 m/s²
ESP32 -> Detect : detectAnomaly(temp=34.5)
Detect --> ESP32 : status = "NORMAL"\n(34.5 < 45, 913 > 850)
ESP32 -> Pipeline : publish(status="NORMAL")

== Scénario Anomalie (Pot = 95%) ==

User -> POT : tourner à 95%
POT --> ESP32 : potPercent = 95
ESP32 -> ESP32 : factor = (95-50)/50 = 0.9\ntemp += 25×0.9 = +22.5°C → 47°C\npress -= 250×0.9 = -225 → 788 hPa\nacc += 20×0.9 = +18 m/s²
ESP32 -> Detect : detectAnomaly(\ntemp=47 > 45 !)
Detect --> ESP32 : status = "ALERT"\nreason = "HIGH TEMP"
ESP32 -> Alert : LED rouge ON\nBuzzer 1500 Hz\nLCD: "HIGH TEMP"
ESP32 -> Pipeline : publish(\nstatus="ALERT",\nreason="HIGH TEMP")

== Scénario Engine Failure (Pot > 80%) ==

ESP32 -> Detect : potPercent = 95 > 80
Detect --> ESP32 : status = "ALERT"\nreason = "ENGINE FAILURE"\n(priorité la plus haute)

@enduml
```

---

## 8. Diagramme de contexte

```plantuml
@startuml
skinparam rectangle {
  BackgroundColor #E3F2FD
  BorderColor #1565C0
  RoundCorner 15
}

actor "Opérateur\nde maintenance" as User
actor "Capteurs\n(DHT22, BMP180,\nMPU6050, Pot)" as Sensors

rectangle "Solution IoT\nMonitoring Aéronautique" as System {
}

cloud "HiveMQ\n(Broker MQTT)" as MQTT
database "InfluxDB 3\n(Stockage TSDB)" as DB
node "Grafana Cloud\n(Dashboard)" as Grafana
node "Module ML\n(Isolation Forest)" as ML

Sensors --> System : données brutes\n(I2C, GPIO, ADC)
System --> MQTT : publication JSON\n(topic: aircraft/sensors)
MQTT --> System : souscription\n(Node-RED)
System --> DB : écriture séries temporelles\n(Line Protocol)
DB --> Grafana : requêtes InfluxQL
DB --> ML : requêtes SQL
ML --> Grafana : alertes anomalies
Grafana --> User : visualisation\n10 panneaux
System --> User : alertes locales\n(LED, Buzzer, LCD)

@enduml
```

---

## Notes sur les corrections apportées

| Élément original | Correction | Justification |
| :--- | :--- | :--- |
| `SQLiteDatabase` | **InfluxDB 3 Core** | Le projet utilise une base de données time series, pas SQLite |
| `Dashboard` (générique) | **Grafana Cloud** (uid: atdh9j, 10 panels) | Dashboard réel du projet |
| `User` (générique) | **Opérateur de maintenance** + **ESP32** | Deux acteurs distincts dans le système |
| `Sensor` (générique) | **DHT22, BMP180, MPU6050, Potentiomètre** | Capteurs spécifiques avec GPIO/I2C réels |
| `ExportService` | **Supprimé** | Fonctionnalité non implémentée dans le projet |
| `ChartService` | **Intégré dans Grafana** | La visualisation est gérée nativement par Grafana |
| `Alert` (générique) | **AlerteLocale** (LED GPIO26/27, Buzzer GPIO25, LCD I2C) | Composants matériels réels |
| `Anomaly` (générique) | **DetectionSeuilsEmbarquée** + **IsolationForest** | Détection à deux niveaux (Edge + Serveur) |
| `Statistics` (classe) | **Intégré dans les requêtes InfluxQL** (mean, min, max) | Calculé par InfluxDB/Grafana |
| Séquence toutes les 5s | **READ=1000ms, MQTT=3000ms, Grafana refresh=5s** | Intervalles réels du firmware |
| `saveAlert()` dans DB | **LED/Buzzer/LCD + MQTT publish** | Les alertes sont locales + transmises via MQTT |
| Topic MQTT absent | **aircraft/sensors** | Topic réel du projet |
| Format JSON absent | **{timestamp, temperature, humidity, pressure, altitude, accX, accY, accZ, potentiometer, status, reason}** | Payload JSON réel (~300 octets) |
