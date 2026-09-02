# CHAPITRE 3 : ANALYSE DES BESOINS ET CONCEPTION DE LA SOLUTION

**Plan du chapitre :**
* Introduction
* 3.1 Identification des besoins
  * 3.1.1 Besoins fonctionnels
  * 3.1.2 Besoins non fonctionnels
* 3.2 Identification des acteurs du système
* 3.3 Architecture détaillée du système
  * 3.3.1 Architecture matérielle
  * 3.3.2 Architecture logicielle
  * 3.3.3 Flux de données
* 3.4 Conception UML
  * 3.4.1 Diagramme de cas d'utilisation
  * 3.4.2 Diagramme de classes
  * 3.4.3 Diagrammes de séquence
* Conclusion

## Introduction

La conception d'un système IoT complexe dédié à la surveillance aéronautique nécessite une analyse rigoureuse et une structuration méthodique. Ce chapitre a pour objectif de détailler la phase d'analyse des besoins et de présenter la conception architecturale de la solution proposée. Nous définirons en premier lieu les exigences fonctionnelles et non fonctionnelles, avant de présenter les différents acteurs interagissant avec le système. Enfin, nous décrirons l'architecture matérielle et logicielle ainsi que la modélisation UML, garantissant ainsi une base solide pour la phase d'implémentation.

## 3.1 Identification des besoins

L'identification des besoins est une étape primordiale pour définir le périmètre du projet et garantir que le système développé répondra aux attentes de la surveillance de l'état de santé des aéronefs (Aircraft Health Monitoring).

### 3.1.1 Besoins fonctionnels

Les besoins fonctionnels décrivent les actions que le système doit impérativement accomplir. Nous les avons modélisés à travers les dix exigences suivantes :

* **BF-01 (Acquisition) :** Le système doit acquérir les données environnementales et cinématiques (température, humidité, pression, altitude, accélération selon les 3 axes) via les capteurs embarqués.
* **BF-02 (Simulation) :** Le système doit permettre la simulation de pannes et d'états critiques via un potentiomètre.
* **BF-03 (Filtrage) :** Le microcontrôleur doit appliquer un filtrage temporel (moyenne mobile) pour lisser les données brutes des capteurs.
* **BF-04 (Détection embarquée) :** Le système doit détecter localement (Edge) des anomalies critiques basées sur des seuils de tolérance.
* **BF-05 (Alerte locale) :** En cas d'anomalie, le système doit déclencher des alertes visuelles (LEDs), sonores (Buzzer) et textuelles (écran LCD).
* **BF-06 (Transmission) :** Les données doivent être formatées en JSON et transmises vers un broker via le protocole MQTT.
* **BF-07 (Routage et Transformation) :** Un middleware doit s'abonner aux flux de données, les parser, les valider et les préparer pour le stockage.
* **BF-08 (Stockage) :** Le système doit stocker les séries temporelles de manière persistante et structurée pour des requêtes analytiques.
* **BF-09 (Visualisation) :** Une interface graphique doit afficher les données en temps réel et l'historique des alertes.
* **BF-10 (Explicabilité ML) :** Bien que non embarqués, les modèles de Machine Learning (Isolation Forest, One-Class SVM, LSTM Autoencoder) entraînés sur le dataset SurveilDrone-Net23 et NASA SMAP/MSL doivent pouvoir ingérer ces données pour des diagnostics complexes.

### 3.1.2 Besoins non fonctionnels

Les besoins non fonctionnels définissent les critères de qualité et les contraintes techniques du système :

* **Fiabilité :** Le système doit garantir l'exactitude des données collectées sans perte de paquets lors de la transmission MQTT (QoS 0 avec gestion des reconnexions).
* **Faible latence :** Les détections d'anomalies embarquées doivent se faire en quasi-temps réel (boucle non bloquante).
* **Robustesse :** Le firmware ne doit pas se bloquer en cas de défaillance d'un capteur.
* **Maintenabilité et Modularité :** Le code doit être structuré en fonctions indépendantes, et l'architecture doit être découplée (Edge, Middleware, Base de données, Dashboard).
* **Scalabilité :** La solution cloud doit pouvoir intégrer de nouveaux nœuds capteurs sans refonte de l'infrastructure.
* **Faible consommation :** L'optimisation des intervalles de lecture et d'envoi contribue à l'efficacité énergétique du dispositif embarqué.

## 3.2 Identification des acteurs du système

Le système interagit avec plusieurs entités que l'on peut qualifier d'acteurs :

* **Opérateur / Ingénieur de maintenance :** Utilisateur final qui consulte les tableaux de bord Grafana et reçoit les alertes de maintenance.
* **Système embarqué (ESP32) :** Acteur physique qui interagit avec l'environnement pour capturer les mesures et exécuter la détection de premier niveau.
* **Broker MQTT (HiveMQ) :** Acteur intermédiaire responsable de la réception et de la distribution des messages de télémétrie.
* **Middleware (Node-RED) :** Acteur de traitement de flux assurant le lien entre le broker et la base de données.
* **Base de données (InfluxDB 3) :** Acteur de persistance spécialisé dans les séries temporelles.

## 3.3 Architecture détaillée du système

### 3.3.1 Architecture matérielle

L'architecture matérielle repose sur un microcontrôleur ESP32, choisi pour sa connectivité Wi-Fi intégrée et sa puissance de calcul (dual-core 240MHz). Les périphériques qui lui sont rattachés sont :
* **Capteur DHT22 (GPIO15) :** Mesure de la température et de l'humidité.
* **Capteur BMP180 (I2C 0x77) :** Mesure de la pression atmosphérique et calcul de l'altitude.
* **Capteur MPU6050 (I2C 0x68) :** Centrale inertielle mesurant l'accélération (X, Y, Z) pour l'analyse vibratoire.
* **Potentiomètre (GPIO34) :** Injecteur de fautes permettant de simuler l'usure ou la défaillance des moteurs.
* **Actionneurs :** Écran LCD 20x4 (I2C), LEDs d'état (Verte = Normal, Rouge = Alerte), et un Buzzer pour les alarmes sonores.

[FIGURE À AJOUTER : Schéma synoptique de l'architecture matérielle sous Wokwi]

### 3.3.2 Architecture logicielle

L'architecture logicielle est distribuée en plusieurs couches (Edge, Fog/Middleware, Cloud) :
* **Couche Edge (Firmware ESP32) :** Développée en C++ (Arduino Core). Elle intègre la gestion des interruptions temporelles via `millis()`, l'échantillonnage, le filtrage, et un système expert à base de règles pour la détection d'anomalies.
* **Couche Middleware (Node-RED) :** Composée de flux (flows) traitant le topic MQTT `aircraft/sensors`. Elle valide les trames JSON et les convertit en points d'insertion (Line Protocol).
* **Couche Persistance (InfluxDB 3) :** Base de données TSDB cloud, configurée avec le bucket `aircraft` et la mesure `sensors`.
* **Couche Présentation (Grafana) :** Interface connectée à InfluxDB exécutant des requêtes InfluxQL pour rafraîchir 10 panneaux analytiques.
* **Pipeline Machine Learning (Cloud/Offline) :** Exploitation de modèles avancés (Isolation Forest 200 arbres, One-Class SVM RBF, et LSTM Autoencoder) exploitant 22 features ingéniérées (ex: `vibration_rms`, `rolling_std`, `temp_z_score`) issus des datasets de référence.

### 3.3.3 Flux de données

Le pipeline de données (Data Pipeline) suit la séquence suivante :
1. **Acquisition** périodique des capteurs (1000 ms).
2. **Filtrage** des valeurs aberrantes de bas niveau (moyenne mobile).
3. **Détection** d'anomalies locale (comparaison de seuils).
4. **Transmission** MQTT toutes les 3000 ms.
5. **Ingestion et Stockage** via Node-RED vers InfluxDB.
6. **Visualisation** sur Grafana (rafraîchissement toutes les 5s).

## 3.4 Conception UML

Le langage UML (Unified Modeling Language) a été utilisé pour standardiser la conception du système.

### 3.4.1 Diagramme de cas d'utilisation

Le diagramme de cas d'utilisation illustre les fonctionnalités offertes à l'utilisateur et aux sous-systèmes. Le cas d'utilisation principal de l'Opérateur est "Surveiller l'état de l'aéronef", qui inclut (include) "Consulter les mesures en temps réel", "Consulter l'historique" et "Recevoir une alerte".

[FIGURE À AJOUTER : Diagramme de cas d'utilisation]

### 3.4.2 Diagramme de classes

Le diagramme de classes représente la structure statique du code embarqué et de l'architecture globale.
* La classe `Sensor` est une super-classe abstraite héritée par `DHT22`, `BMP180` et `MPU6050`.
* La classe `Filter` applique les algorithmes mathématiques aux objets `Measurement`.
* La classe `AnomalyDetector` génère des objets `Alert`.
* La classe `MQTTClient` gère la sérialisation JSON et la publication réseau.

[FIGURE À AJOUTER : Diagramme de classes]

### 3.4.3 Diagrammes de séquence

Le diagramme de séquence de la **Détection d'anomalies et Transmission** illustre l'aspect temporel.
1. La boucle principale invoque les objets capteurs.
2. Les données transitent par le filtre.
3. Le détecteur évalue les règles. S'il détecte une vibration > 15 m/s², il active l'alarme locale.
4. L'objet MQTTClient formate le payload JSON avec `status: ALERT` et le publie sur HiveMQ.

[FIGURE À AJOUTER : Diagramme de séquence de l'acquisition à l'alerte]

## Conclusion

Ce chapitre a permis de définir avec précision les attentes fonctionnelles et structurelles de notre système de surveillance aéronautique. En détaillant l'architecture multi-tiers (matériel, logiciel embarqué, middleware, cloud) et en proposant une modélisation UML rigoureuse, nous avons établi un cahier des charges technique exhaustif. Ce socle conceptuel servira de fil conducteur pour le chapitre suivant, dédié à la réalisation concrète et à l'implémentation de la solution.

---

# CHAPITRE 4 : RÉALISATION ET IMPLÉMENTATION

**Plan du chapitre :**
* Introduction
* 4.1 Environnement matériel et logiciel
* 4.2 Implémentation du module d'acquisition
* 4.3 Implémentation du filtrage des données
* 4.4 Implémentation du module de détection d'anomalies
* 4.5 Mise en place de la communication MQTT
* 4.6 Mise en place du stockage des données (InfluxDB)
* 4.7 Développement de l'interface de monitoring (Grafana)
* 4.8 Gestion des erreurs et des logs
* 4.9 Problèmes techniques rencontrés et solutions
* 4.10 Tests et validation
* Conclusion

## Introduction

La phase d'implémentation constitue la concrétisation des concepts architecturaux définis précédemment. Ce chapitre détaille la réalisation technique du projet, du codage du firmware sur le microcontrôleur à la configuration des services cloud (InfluxDB et Grafana), en passant par le développement du middleware Node-RED. Nous mettrons particulièrement l'accent sur les solutions techniques adoptées, la robustesse du code, les problèmes rencontrés lors de l'intégration et les scénarios de validation.

## 4.1 Environnement matériel et logiciel

Pour garantir la reproductibilité et la fiabilité du prototypage, nous avons utilisé les environnements suivants :
* **Matériel :** ESP32 DevKit C v4 (microcontrôleur dual-core à 240 MHz, 520 Ko SRAM) simulé de manière déterministe via la plateforme Wokwi.
* **Logiciels et Outils :**
  * Arduino IDE pour le développement C++.
  * Node-RED pour le middleware IoT.
  * InfluxDB 3 Core (v3.11.0) pour la base de données chronologique.
  * Grafana Cloud (v13.2.0) pour la visualisation.
* **Bibliothèques C++ exploitées :** `Wire.h`, `WiFi.h`, `PubSubClient.h`, `DHT.h`, `Adafruit_BMP085.h`, `Adafruit_MPU6050.h`, et `LiquidCrystal_I2C.h`.

Le firmware a été conçu pour être **100% non bloquant**. L'utilisation de la fonction `millis()` a permis de gérer les tâches de manière asynchrone avec les intervalles suivants :
* Acquisition des capteurs (`READ`) : 1000 ms.
* Mise à jour de l'écran LCD (`LCD`) : 1000 ms.
* Affichage de débogage (`SERIAL`) : 2000 ms.
* Transmission MQTT (`MQTT`) : 3000 ms.

## 4.2 Implémentation du module d'acquisition

Le module d'acquisition collecte les données via des bus de communication spécifiques. Les fonctions `readTemperature()` et `readHumidity()` interrogent le DHT22 avec une vérification stricte via `isnan()` pour prévenir les erreurs de lecture. Le BMP180 communique en I2C (0x77), fournissant la pression (convertie en hPa via une division par 100.0) et l'altitude relative (basée sur une pression de référence de 1013.25 hPa). Le MPU6050 (0x68) fournit les événements d'accélération via `getEvent()`.

Une fonctionnalité majeure de notre acquisition est la **simulation d'injection de fautes**. La fonction `analogRead()` lit le potentiomètre (0-4095), mappé en pourcentage (0-100%).
Si le pourcentage dépasse 50%, un facteur de dégradation est appliqué artificiellement aux lectures des capteurs :
```cpp
if (potPercent > 50) {
  float factor = (potPercent - 50) / 50.0;
  temp += 25 * factor;
  pressure -= 250 * factor;
  altitude += 1500 * factor;
  accX += 20 * factor;
}
```

## 4.3 Implémentation du filtrage des données

Pour pallier le bruit de mesure inhérent aux capteurs environnementaux, un filtre de moyenne mobile a été implémenté en mémoire locale sur l'ESP32.

```cpp
#define FILTER_SIZE 5
float tempBuffer[FILTER_SIZE];
// [...]
float movingAverage(float* buffer, float newValue) {
  float sum = 0;
  for(int i = FILTER_SIZE - 1; i > 0; i--) {
    buffer[i] = buffer[i-1];
    sum += buffer[i];
  }
  buffer[0] = newValue;
  sum += newValue;
  return sum / FILTER_SIZE;
}
```
Ce filtrage permet de lisser les pics aléatoires (notamment sur l'accéléromètre), réduisant ainsi les faux positifs lors de l'étape de détection.

## 4.4 Implémentation du module de détection d'anomalies

La détection locale s'appuie sur un arbre de décision basé sur des règles de priorité critiques. Le calcul de la vibration globale s'effectue en extrayant la magnitude du vecteur d'accélération (corrigé de la gravité spatiale) : `vibration = sqrt(ax² + ay² + (az-9.8)²)`

Les seuils sont évalués de manière hiérarchique :
1. **HIGH TEMP :** Température > 45°C.
2. **LOW PRESSURE :** Pression < 850 hPa.
3. **HIGH VIBRATION :** Vibration > 15 m/s².
4. **ENGINE FAILURE :** Potentiomètre > 80%.

En cas d'anomalie, le système désactive la LED verte, active la LED rouge, déclenche le buzzer à 1500 Hz, affiche la raison sur l'écran LCD, et prépare le statut MQTT à `ALERT`.

## 4.5 Mise en place de la communication MQTT

La couche de communication repose sur `PubSubClient`. La taille du buffer a été augmentée à 512 octets via `client.setBufferSize(512)` pour supporter des payloads JSON d'environ 300 octets.
Le client se connecte au broker public `broker.hivemq.com` sur le port 1883. Afin d'éviter les conflits entre plusieurs nœuds, un identifiant de client unique est généré en concaténant l'adresse MAC de l'ESP32 (`AircraftESP32-[MAC]`).

Le payload transmis est structuré au format JSON natif :
```json
{
  "timestamp": 1718290000,
  "temperature": 46.5,
  "humidity": 35.0,
  "pressure": 845.2,
  "altitude": 1400,
  "accX": 1.2,
  "accY": -0.5,
  "accZ": 10.1,
  "potentiometer": 85,
  "status": "ALERT",
  "reason": "LOW PRESSURE"
}
```

## 4.6 Mise en place du stockage des données (InfluxDB)

Le flux de données transite par Node-RED. Le flux principal (`mqtt_in` → `fn_parse_validate` → `fn_to_influx_points` → `influx_out`) s'abonne au topic `aircraft/sensors` avec une QoS de 0.
La fonction de transformation prépare les objets au format requis par InfluxDB 3 :
* **Measurement :** `sensors`
* **Tags :** `device=ESP32`
* **Fields :** temperature, humidity, pressure, etc.

La persistance dans InfluxDB se fait via des requêtes HTTP POST sur l'endpoint `/api/v2/write`. Les données stockées peuvent ensuite être interrogées via l'endpoint `/query` en utilisant le langage InfluxQL.

## 4.7 Développement de l'interface de monitoring (Grafana)

Le tableau de bord Grafana centralise la supervision opérationnelle. Nous avons conçu 10 panneaux distincts (Panels) :
* 4 graphiques de séries temporelles (Time series) pour la Température, l'Humidité, la Pression et l'Altitude.
* 1 graphique tridimensionnel pour les accélérations (X, Y, Z).
* 1 jauge (Gauge) pour surveiller le potentiomètre (niveau d'usure/simulation).
* 4 panneaux statistiques (Stat panels) indiquant l'état instantané du système.

L'interfaçage avec la base de données s'effectue via un tunnel *ngrok*, nécessitant une configuration en mode **InfluxQL** pour garantir la compatibilité réseau (taux de rafraîchissement défini à 5 secondes).

[CAPTURE À INSÉRER : Tableau de bord Grafana en mode nominal]
[CAPTURE À INSÉRER : Tableau de bord Grafana affichant une alerte]

## 4.8 Gestion des erreurs et des logs

La robustesse du firmware repose sur une gestion avancée des erreurs :
* **Dédoublonnage LCD :** Pour éviter le scintillement (flickering), le code compare la chaîne courante (`currentDisplay`) avec la dernière chaîne affichée (`lastDisplay`) avant de rafraîchir l'écran.
* **Fallback Temporel (NTP) :** Si la synchronisation NTP échoue au démarrage, le système bascule automatiquement sur un horodatage local calculé via `millis()`.
* **Supervision Série :** Des logs formatés sont envoyés au moniteur série toutes les 2 secondes pour faciliter le débogage de l'opérateur.

## 4.9 Problèmes techniques rencontrés et solutions

La phase de réalisation a été marquée par plusieurs défis techniques qui ont nécessité des ajustements architecturaux, résumés dans le tableau suivant :

| ID | Problème rencontré | Cause identifiée | Solution apportée |
| :--- | :--- | :--- | :--- |
| **D1** | Trame JSON vide dans Node-RED | Interruption réseau momentanée | Ajout d'une validation JS robuste dans `fn_parse_validate`. |
| **D2** | Gel total du microcontrôleur au démarrage | Boucle `while(!Serial)` infinie si câble débranché | Suppression de l'instruction bloquante. |
| **D3** | BMP180 affichant 47750 Pa au lieu de 101325 Pa | Mauvaise configuration du modèle dans Wokwi | Correction de la référence de base dans `diagram.json`. |
| **D4** | Incompatibilité de connexion Grafana / InfluxDB | Protocole gRPC bloqué par la version de ngrok | Passage de l'API au mode InfluxQL. |
| **D5** | Erreur d'authentification InfluxDB (401 Unauthorized) | Token corrompu ou expiré dans Node-RED | Injection directe du token via les paramètres de l'API POST. |
| **D6** | Déconnexions aléatoires du tunnel ngrok | Version obsolète du client | Mise à jour du daemon ngrok à la version 3.39.10. |
| **D7** | Conflit et déconnexion en boucle sur le MQTT (HiveMQ) | Utilisation du même Client ID par plusieurs instances | Génération dynamique de l'ID via `WiFi.macAddress()`. |

*Tableau 4.1 : Synthèse des problèmes techniques et solutions appliquées*

## 4.10 Tests et validation

Pour certifier le bon fonctionnement du pipeline de données, un protocole de test rigoureux a été exécuté. Le firmware a passé avec succès les tests unitaires des fonctions internes (`movingAverage`, `readSensors`, `sendMQTT`).

Des tests d'intégration ont été réalisés en injectant différents niveaux de fautes via le potentiomètre :

| Scénario | Potentiomètre (%) | Valeurs simulées | Comportement attendu | Résultat obtenu |
| :--- | :--- | :--- | :--- | :--- |
| **Normal** | 0% | Temp: ~25°C, Press: ~1013hPa | Status: NORMAL, LED Verte | Validé |
| **High Temp** | 95% | Temp = 47.5°C | Status: HIGH TEMP, LED Rouge | Validé |
| **Low Pressure**| 85% | Pression = 838 hPa | Status: LOW PRESSURE, Buzzer | Validé |
| **High Vibration**| 80% | Accel Z compensé > 17 m/s² | Status: HIGH VIBRATION | Validé |
| **Engine Failure**| 90% | Potentiomètre > 80% | Status: ENGINE FAILURE | Validé |

*Tableau 4.2 : Scénarios de tests de la logique de détection des anomalies*

L'API InfluxDB a été testée via des requêtes de santé (health check) et des requêtes SQL/InfluxQL manuelles, confirmant la persistance continue des `1 measurements` au sein de la base.

## Conclusion

Ce chapitre a illustré le processus de concrétisation de notre système de surveillance aéronautique IoT. Grâce à l'emploi d'un code C++ hautement optimisé (non bloquant, filtré) et au paramétrage précis des intermédiaires cloud, nous avons réussi à établir un pipeline de bout en bout fiable. Les tests de validation confirment la capacité du système à réagir en quasi-temps réel aux anomalies générées, remplissant ainsi pleinement le cahier des charges. Ces résultats probants ouvrent la voie à l'exploitation des données collectées par nos modèles d'intelligence artificielle.
