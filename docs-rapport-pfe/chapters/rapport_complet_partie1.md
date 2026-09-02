# RAPPORT DE PROJET DE FIN D'ÉTUDES
**Stagiaire :** Nourhen KHELIFI
**Entreprise :** YaneCode Digital — Aeronautics & Embedded Systems
**Référence :** CDC_2026_NourhenKHELIFI_YC_ES20268812
**Période :** Été 2026 (Avancement 87%)

---

## RÉSUMÉ

Ce rapport présente la conception et la réalisation d'un système embarqué complet dédié à la surveillance et à la maintenance prédictive dans le domaine de l'aéronautique et des systèmes embarqués. Développé au sein de l'entreprise YaneCode Digital, ce projet propose une architecture à cinq couches allant de l'acquisition de données par des capteurs (température, pression, accélération) jusqu'à leur visualisation sur un tableau de bord interactif. Le cœur du système repose sur un microcontrôleur ESP32 programmé en C++ de manière totalement non bloquante, assurant une acquisition fiable et un filtrage par moyenne glissante. La transmission des données est assurée par le protocole MQTT vers un broker public, avant d'être traitées par un middleware Node-RED. Le stockage persistant est confié à une base de données temporelle InfluxDB, et la visualisation est réalisée via Grafana Cloud. Les résultats obtenus démontrent la robustesse du système face aux anomalies, avec une détection locale permettant de déclencher des alertes immédiates (LEDs, Buzzer, LCD) et une latence de bout en bout inférieure à trois secondes. 

**Mots-clés :** Internet des Objets (IoT), Aéronautique, ESP32, MQTT, Node-RED, InfluxDB, Grafana, Maintenance prédictive.

## ABSTRACT

This report presents the design and implementation of a comprehensive embedded system dedicated to monitoring and predictive maintenance in the field of aeronautics and embedded systems. Developed at YaneCode Digital, this project proposes a five-layer architecture ranging from data acquisition by sensors (temperature, pressure, acceleration) to their visualization on an interactive dashboard. The core of the system relies on an ESP32 microcontroller programmed in C++ in a completely non-blocking manner, ensuring reliable acquisition and moving average filtering. Data transmission is handled by the MQTT protocol to a public broker, before being processed by a Node-RED middleware. Persistent storage is entrusted to a time-series database, InfluxDB, and visualization is performed via Grafana Cloud. The results obtained demonstrate the robustness of the system against anomalies, with local detection triggering immediate alerts (LEDs, Buzzer, LCD) and an end-to-end latency of less than three seconds.

**Keywords :** Internet of Things (IoT), Aeronautics, ESP32, MQTT, Node-RED, InfluxDB, Grafana, Predictive maintenance.

---

## INTRODUCTION GÉNÉRALE

Le secteur de l'aéronautique exige des niveaux de sécurité et de fiabilité maximaux, où la moindre défaillance matérielle peut avoir des conséquences critiques. Dans ce contexte, la maintenance prédictive s'impose comme une stratégie incontournable pour anticiper les pannes avant qu'elles ne surviennent. L'Internet des Objets (IoT) offre des solutions technologiques novatrices permettant la remontée en temps réel de données physiologiques des équipements, ouvrant ainsi la voie à une surveillance continue et intelligente.

La problématique principale de ce projet réside dans la capacité à concevoir une chaîne d'acquisition et de traitement de données qui soit à la fois robuste, réactive et modulaire. Il s'agit de capter des grandeurs physiques critiques telles que la température, la pression atmosphérique, l'altitude et les vibrations, de les filtrer pour éliminer le bruit, et de détecter localement toute anomalie afin de réagir en temps réel. Par ailleurs, ces données doivent être transmises de manière sécurisée et fiable vers une plateforme centralisée pour un archivage historique et une analyse visuelle approfondie.

Pour répondre à ce défi, l'objectif principal de ce projet est de développer un système IoT complet reposant sur une architecture en cinq couches : l'acquisition via un microcontrôleur ESP32, la transmission par messagerie MQTT, le routage via Node-RED, le stockage optimisé avec InfluxDB, et la restitution visuelle sous Grafana. Ce système inclut également un mécanisme de simulation d'anomalies via un potentiomètre afin de valider les scénarios de défaillance (surchauffe, dépressurisation, vibrations excessives, panne moteur).

La méthodologie adoptée tout au long de ce projet s'appuie sur l'approche Agile Kanban. Cette méthode a permis une gestion fluide et itérative des tâches, garantissant une adaptation continue aux contraintes techniques rencontrées et une visibilité constante sur l'état d'avancement du projet. 

Ce rapport s'organise en quatre chapitres principaux. Le premier chapitre dresse le contexte général, analyse les solutions existantes et formalise le cahier des charges. Le deuxième chapitre est consacré à l'état de l'art et justifie rigoureusement les choix technologiques retenus à chaque niveau de l'architecture. Le troisième chapitre détaille l'analyse des besoins et propose une conception conceptuelle et architecturale du système. Enfin, le quatrième chapitre décrit la réalisation technique, l'implémentation du code, ainsi que les phases de tests et de validation ayant permis de surmonter les divers défis techniques.

---

## CHAPITRE 1 — Contexte général, étude de l'existant et cahier des charges

Ce chapitre a pour vocation de poser les bases du projet. Dans un premier temps, le cadre d'accueil du stage est présenté. Ensuite, le contexte et la problématique sont détaillés, suivis d'une analyse critique des solutions existantes sur le marché. Enfin, le cahier des charges technique est défini avec précision, encadré par la méthodologie de gestion de projet adoptée.

### 1.1 Présentation de YaneCode Digital
Le présent projet de fin d'études s'est déroulé au sein de l'entreprise YaneCode Digital, une structure spécialisée dans l'ingénierie logicielle et les systèmes embarqués appliqués au domaine de l'aéronautique (Aeronautics & Embedded Systems). L'entreprise se distingue par sa volonté d'intégrer des technologies de pointe pour moderniser les infrastructures de maintenance et optimiser la gestion des flottes aériennes ou des équipements industriels critiques.

### 1.2 Contexte du projet
Dans le monde industriel moderne, et particulièrement en aéronautique, la maintenance curative traditionnelle montre ses limites face aux impératifs de rentabilité et de sécurité. L'émergence des capteurs à bas coût et des réseaux de communication sans fil permet désormais de basculer vers une maintenance prédictive. L'idée est de doter les équipements d'une intelligence embarquée capable de mesurer leur état de santé en continu, d'identifier les prémices d'une défaillance et de remonter ces informations vers des centres de contrôle pour une prise de décision anticipée.

### 1.3 Problématique
Malgré les avancées technologiques, la conception d'un tel système soulève plusieurs défis majeurs. Comment garantir une acquisition de données sans blocage du processeur pour ne pas perdre d'informations critiques ? Comment filtrer le bruit inhérent aux capteurs environnementaux et inertiels ? Comment assurer une transmission fluide et à faible latence des données vers le cloud tout en gérant les déconnexions réseau ? Enfin, comment stocker et visualiser efficacement des flux de données temporelles à haute fréquence de manière à fournir un tableau de bord exploitable par un opérateur de maintenance ? C'est à cet ensemble de questions que notre projet se propose de répondre de manière systématique et intégrée.

### 1.4 Étude et critique de l'existant
Les solutions actuelles de surveillance industrielle sont souvent basées sur des architectures monolithiques et propriétaires. Ces systèmes fermés présentent un coût d'acquisition et de maintenance extrêmement élevé, tout en offrant une flexibilité très limitée pour l'intégration de nouveaux capteurs ou l'évolution vers le cloud. De plus, de nombreuses implémentations d'entrée de gamme utilisent des boucles de programmation bloquantes, ce qui empêche le traitement simultané de plusieurs tâches critiques (comme lire un capteur tout en envoyant un message réseau). Notre solution se démarque par son approche modulaire (microservices, middleware), l'utilisation de protocoles standards ouverts (MQTT) et un firmware totalement asynchrone.

### 1.5 Cahier des charges détaillé
Le système à concevoir doit répondre à un ensemble d'exigences strictes. Il doit être capable de mesurer la température, l'humidité, la pression, l'altitude et l'accélération tridimensionnelle. Le système embarqué doit appliquer un filtrage numérique localement et comparer les valeurs filtrées à des seuils d'alerte prédéfinis. En cas de dépassement, une signalisation locale (visuelle et sonore) doit être activée, et un message d'erreur doit être formaté et transmis. Du côté serveur, les données doivent être réceptionnées, validées, converties en points de mesure et stockées dans une base de données temporelle. Une interface graphique doit ensuite requêter cette base pour afficher les séries temporelles et l'état global du système avec un rafraîchissement régulier.

### 1.6 Méthodologie de travail (Kanban)
Pour mener à bien ce projet, la méthodologie Kanban a été adoptée. Elle a permis de diviser la réalisation en un flux continu de tâches (À faire, En cours, Test, Terminé), maximisant ainsi la réactivité face aux imprévus. Cette approche s'est révélée particulièrement efficace lors de la résolution de problèmes techniques complexes, permettant de focaliser les efforts sur les bloqueurs (goulets d'étranglement) avant d'entamer de nouvelles fonctionnalités. L'avancement actuel du projet est évalué à 87%, reflétant l'achèvement réussi des phases de conception, d'implémentation et des tests majeurs.

### Conclusion du chapitre
Ce premier chapitre a permis de délimiter le périmètre du projet. En partant d'un constat sur les limites de l'existant, un cahier des charges ambitieux a été défini, structuré autour d'une approche agile. Les bases étant posées, le chapitre suivant s'attachera à étudier les technologies disponibles pour répondre à ces exigences.

---

## CHAPITRE 2 — État de l'art et justification des choix technologiques

Ce chapitre expose un panorama des technologies existantes pour chaque composant de l'architecture. À travers des analyses comparatives, il justifie les choix matériels, logiciels et protocolaires qui constituent la colonne vertébrale du système mis en œuvre.

### 2.1 L'Internet des Objets (IoT) dans le domaine industriel
L'IoT industriel (IIoT) consiste en un réseau de capteurs, d'instruments et de dispositifs autonomes connectés via Internet à des applications industrielles. Il se distingue de l'IoT grand public par des exigences très strictes en termes de robustesse, de sécurité, de fiabilité et de latence. Dans notre contexte aéronautique, l'IIoT permet de digitaliser les paramètres physiques des aéronefs pour alimenter des algorithmes de maintenance prédictive.

### 2.2 Comparaison et choix des cartes embarquées
Le choix du microcontrôleur est une étape critique. Plusieurs alternatives ont été étudiées, notamment l'Arduino Uno, le Raspberry Pi Zero, les cartes STM32 et l'ESP32. 

| Critère | Arduino Uno | Raspberry Pi Zero | STM32 | ESP32 DevKit C v4 |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | 8-bit, 16 MHz | 32-bit, 1 GHz | 32-bit, 84 MHz | 32-bit Dual-core, 240 MHz |
| **Mémoire RAM** | 2 KB | 512 MB | 96 KB | 520 KB |
| **Connectivité intégrée** | Aucune | Wi-Fi, Bluetooth | Aucune (généralement) | Wi-Fi, Bluetooth (BLE) |
| **Simulation Wokwi** | Supportée | Partielle/Non | Limitée | Support complet |
| **Coût estimé** | Faible | Moyen | Moyen | Faible |

Le microcontrôleur ESP32 DevKit C v4 s'impose comme la solution optimale. Son processeur double cœur à 240 MHz offre une puissance de calcul amplement suffisante pour le filtrage et la connectivité réseau simultanés. Sa connectivité Wi-Fi native est indispensable pour l'envoi des données, et sa prise en charge totale par le simulateur Wokwi facilite le prototypage.

### 2.3 Comparaison et choix des capteurs
Pour répondre aux besoins d'acquisition, trois capteurs principaux ont été sélectionnés pour leurs caractéristiques adaptées aux environnements exigeants. Le DHT22 (connecté sur le GPIO15) permet de mesurer une température allant de -40 à +80°C avec une précision de ±0.5°C, ainsi que l'humidité relative de 0 à 100%. Le BMP180 (bus I2C, adresse 0x77) fournit des relevés de pression précis (de 300 à 1100 hPa) et permet de déduire l'altitude relative en se basant sur une pression de référence fixée à 1013.25 hPa. Enfin, le module MPU6050 (bus I2C, adresse 0x68) intègre un accéléromètre trois axes essentiel pour analyser les vibrations du système en mètres par seconde au carré (m/s²). L'ajout d'un potentiomètre sur l'ADC (GPIO34) converti sur 12 bits (mappé de 0 à 100%) sert à l'injection contrôlée de défauts simulés.

### 2.4 Techniques de filtrage numérique
Les signaux issus des capteurs MEMS (comme le MPU6050) et environnementaux sont naturellement bruités. Pour stabiliser les mesures avant analyse, un filtre à moyenne glissante a été privilégié par rapport à des approches plus complexes comme le filtre de Kalman. La moyenne glissante consiste à stocker les dernières valeurs acquises dans un tableau (buffer) et à en calculer la moyenne arithmétique. Cette méthode présente l'avantage d'une implémentation algorithmique très légère, particulièrement adaptée aux contraintes de mémoire de l'ESP32, tout en lissant efficacement les variations sporadiques de haute fréquence.

### 2.5 Détection d'anomalies embarquée
L'intelligence à la périphérie (Edge Computing) est essentielle pour garantir un temps de réaction minimal. Plutôt que de déléguer l'analyse complète au serveur distant, le système embarqué intègre une logique de détection par seuillage. Les règles métier sont évaluées localement à chaque cycle d'acquisition. Cette approche hybride garantit que les alertes critiques de niveau 1 (comme une surchauffe soudaine ou une vibration anormale) déclenchent instantanément des actionneurs locaux (LEDs, Buzzer, LCD) sans dépendre de la latence du réseau ou de la disponibilité du broker cloud.

### 2.6 Protocoles de communication : le choix de MQTT
La remontée des données télémétriques nécessite un protocole de transport efficace.

| Critère | HTTP / REST | WebSocket | CoAP | MQTT (v3.1.1) |
| :--- | :--- | :--- | :--- | :--- |
| **Modèle de communication** | Requête/Réponse | Bidirectionnel | Requête/Réponse | Publication/Souscription |
| **Overhead (En-tête)** | Lourd | Moyen | Faible | Très faible (2 octets minimum) |
| **Gestion des déconnexions** | Manuelle | Manuelle | Native (partielle) | Intégrée (QoS, LWT) |

Le protocole MQTT en version 3.1.1 s'est imposé comme le standard de facto pour ce projet. Son architecture en mode publication/souscription (Publish/Subscribe) découple totalement les producteurs de données (ESP32) des consommateurs (Node-RED). L'utilisation d'une Qualité de Service de niveau 0 (QoS 0) a été retenue pour maximiser le débit, considérant que la perte occasionnelle d'un échantillon à haute fréquence est moins critique qu'un ralentissement du système dû aux accusés de réception. Le serveur public HiveMQ (`broker.hivemq.com` sur le port 1883) assure le rôle de broker.

### 2.7 Base de données temporelle : InfluxDB
Le stockage des mesures historiques requiert une base de données spécialisée dans le traitement des séries temporelles (Time Series Database - TSDB). Contrairement aux bases de données relationnelles classiques comme SQLite, ou aux outils de supervision système comme Prometheus, InfluxDB a été sélectionnée. Dans sa version 3 Core (v3.11.0, hébergée en local sur le port 8181), elle offre une structure de données optimisée par `bucket`, `measurement` et `tags`, garantissant une indexation performante. Bien que TimescaleDB soit une alternative robuste basée sur PostgreSQL, InfluxDB propose une intégration plus fluide et native avec le reste de l'écosystème Node-RED et Grafana.

### 2.8 Plateforme de visualisation : Grafana
Pour l'exploitation visuelle des données, Grafana Cloud (v13.2.0) a été choisi face à des concurrents comme Kibana, Tableau ou Power BI. Kibana est intrinsèquement lié à l'écosystème ElasticSearch, tandis que Tableau et Power BI s'orientent davantage vers la Business Intelligence statique. Grafana excelle dans le rafraîchissement dynamique et la supervision d'infrastructures IoT, offrant des panneaux hautement configurables et une compatibilité directe avec le langage de requête d'InfluxDB.

### 2.9 Environnement de simulation : Wokwi
La réalisation matérielle de ce projet a été virtualisée à l'aide de Wokwi, un simulateur en ligne avancé. Face à Proteus (lourd, onéreux et orienté schématique classique), SimulIDE ou TinkerCAD (trop basique, support limité de l'ESP32 et du Wi-Fi), Wokwi permet d'exécuter le firmware C++ compilé pour l'ESP32 avec un support réseau fonctionnel, reproduisant fidèlement les comportements du Wi-Fi et de la pile TCP/IP nécessaires à MQTT.

### Conclusion du chapitre
Cette phase d'étude de l'existant a permis d'opérer des choix technologiques éclairés. L'architecture s'articule autour d'un ESP32 simulé sous Wokwi, communiquant via MQTT vers un flux Node-RED, avec un stockage InfluxDB et une supervision Grafana. Le chapitre suivant va s'attacher à définir la structure formelle de cette architecture à travers une analyse détaillée des besoins.

---

## CHAPITRE 3 — Analyse des besoins et conception

Ce chapitre constitue la phase d'ingénierie logicielle et système. Il traduit le cahier des charges en besoins formels, identifie les acteurs, structure les architectures matérielles et logicielles, et formalise le comportement du système à l'aide du langage de modélisation UML.

### 3.1 Expression des besoins fonctionnels
Les fonctionnalités attendues du système ont été cataloguées rigoureusement pour guider le développement.

| Identifiant | Description du besoin fonctionnel |
| :--- | :--- |
| **BF-01** | Le système doit acquérir les données des capteurs DHT22, BMP180 et MPU6050 à une fréquence définie (1000ms). |
| **BF-02** | Le système doit acquérir la valeur du potentiomètre (0-100%) pour servir de variateur de défaut simulé. |
| **BF-03** | Le microcontrôleur doit appliquer un filtre de moyenne glissante sur une fenêtre de 5 échantillons. |
| **BF-04** | Le système doit détecter localement les anomalies basées sur des seuils critiques prédéfinis. |
| **BF-05** | En cas d'anomalie, des alertes locales (LED rouge, Buzzer, message LCD) doivent être déclenchées. |
| **BF-06** | Le firmware doit formater toutes les données acquises et l'état d'alerte dans un objet JSON structuré. |
| **BF-07** | L'ESP32 doit transmettre la charge utile JSON via MQTT vers le topic désigné. |
| **BF-08** | Le middleware doit réceptionner, valider l'intégrité du JSON et le convertir en points de mesure. |
| **BF-09** | Les données converties doivent être insérées et stockées de manière persistante dans la base temporelle. |
| **BF-10** | Un tableau de bord dynamique doit requêter la base de données pour visualiser les séries temporelles en temps réel. |

### 3.2 Expression des besoins non fonctionnels
Au-delà des fonctionnalités, le système doit satisfaire des critères de performance et de qualité stricts.

| Identifiant | Description du besoin non fonctionnel |
| :--- | :--- |
| **BNF-01** | **Fiabilité :** Le système ne doit comporter aucune boucle bloquante empêchant l'exécution des autres tâches. |
| **BNF-02** | **Faible latence :** Le délai entre l'apparition d'un défaut physique et son affichage sur le cloud doit être inférieur à 3 secondes. |
| **BNF-03** | **Robustesse :** Le système doit gérer automatiquement les reconnexions au réseau Wi-Fi et au broker MQTT. |
| **BNF-04** | **Maintenabilité et Modularité :** Le code C++ doit être organisé en fonctions distinctes, et l'architecture globale en couches indépendantes. |
| **BNF-05** | **Scalabilité :** La base de données et le tableau de bord doivent pouvoir ingérer des données provenant de multiples capteurs simultanément. |

### 3.3 Identification des acteurs
Plusieurs entités, humaines ou machines, interagissent avec le système. L'**Opérateur de maintenance** est l'utilisateur final qui consulte le tableau de bord pour superviser l'état de l'aéronef. L'**ESP32 (Système embarqué)** agit comme l'acteur principal de terrain, collectant et traitant l'information. Le **Broker MQTT** agit en tant que facilitateur de transport. Le **Module de détection** (intégré au firmware) prend les décisions critiques locales. Enfin, la **Base de données** et le **Dashboard** assurent la persistance et la présentation.

### 3.4 Architecture matérielle globale
L'architecture matérielle se concentre autour du nœud d'acquisition. Le microcontrôleur ESP32 DevKit C v4 centralise les connexions. Les capteurs environnementaux et inertiels (DHT22, BMP180, MPU6050) lui transmettent leurs signaux via les bus I2C et broches GPIO numériques. Les actionneurs de signalisation comprennent un écran LCD 20x4, une LED verte témoin de fonctionnement normal, une LED rouge signalant un état critique, et un buzzer piézoélectrique. L'interface d'injection de défaut est matérialisée par un potentiomètre linéaire.

### 3.5 Architecture logicielle
Le système logiciel est fondé sur un paradigme de traitement distribué. Au niveau du nœud, le firmware est architecturé autour d'un ordonnanceur coopératif basé sur la fonction `millis()`, garantissant un fonctionnement multitâche. Au niveau du middleware, le moteur de flux Node-RED orchestre le transit des messages entre le monde MQTT (abonnement au topic `aircraft/sensors`) et le monde des bases de données. Ce flux inclut des nœuds de fonction en JavaScript dédiés à la validation des trames et à la préparation des requêtes d'insertion.

### 3.6 Flux de données
Le cycle de vie de la donnée débute par l'échantillonnage brut. Ces signaux subissent un filtrage, suivi d'une évaluation par le moteur de règles local (détection de seuils). Les données consolidées et estampillées (horodatage NTP UTC+1) sont sérialisées au format JSON (environ 300 octets par payload). Ce document transite par le réseau TCP/IP via MQTT. Node-RED désérialise le message, extrait les champs (température, humidité, pression, etc.) et les métadonnées (statut, raison, identifiant MAC). Il construit ensuite un objet InfluxDB contenant la `measurement`, les `tags` et les `fields`, qui est finalement propulsé dans le bucket via une requête HTTP/1.1 (InfluxQL) via un tunnel ngrok sécurisé.

### 3.7 Conception modélisée (UML)
Afin de formaliser les structures et les interactions logicielles, des diagrammes UML ont été élaborés.

Le **diagramme des cas d'utilisation** illustre les interactions principales. L'opérateur peut consulter les données et recevoir des alertes. Le système embarqué acquiert, filtre et transmet l'information, tout en pilotant les alertes locales.

[FIGURE À AJOUTER : Diagramme des cas d'utilisation UML]

Le **diagramme de classes** décrit la structure orientée objet du firmware et du backend. Il intègre les classes matérielles (ESP32, DHT22, BMP180, MPU6050), les structures de données (MesureJSON), les entités de traitement (DetectionSeuils, AlerteLocale), les gestionnaires de communication (MQTTClient) et les composants serveurs (NodeRED, InfluxDB, GrafanaDashboard). L'intégration future de modèles prédictifs est matérialisée par une classe IsolationForest.

[FIGURE À AJOUTER : Diagramme de classes UML]

Le **diagramme de séquences** chronologique met en évidence les trois phases principales : l'acquisition cyclique (interrogation des bus, filtrage tempBuffer), la détection asynchrone (évaluation des seuils et déclenchement immédiat des interruptions ou flags), et la consultation (flux de données traversant MQTT, Node-RED, InfluxDB, jusqu'au rafraîchissement Grafana).

[FIGURE À AJOUTER : Diagramme de séquences UML]

### Conclusion du chapitre
Les spécifications et l'architecture du projet étant désormais formellement établies et modélisées, toutes les conditions préalables au développement sont réunies. Le chapitre suivant s'immergera dans la réalisation concrète, détaillant le code source, les configurations serveurs et le processus de validation technique.

---

## CHAPITRE 4 — Réalisation et implémentation

Ce dernier chapitre de la première partie aborde le cœur technique du projet. Il présente l'environnement de développement, détaille l'implémentation du code C++ embarqué (firmware), la configuration de la chaîne de transmission et du stockage, la mise en place du tableau de bord, ainsi que la résolution des anomalies techniques rencontrées durant l'intégration.

### 4.1 Environnement matériel et logiciel

L'ensemble des outils mobilisés pour la conception de ce système est récapitulé dans le tableau suivant :

| Composant | Technologie / Outil utilisé |
| :--- | :--- |
| **Simulateur matériel** | Wokwi (Plateforme Cloud) |
| **Langage Firmware** | C++ (Framework Arduino) |
| **Broker MQTT** | HiveMQ (Public - broker.hivemq.com) |
| **Middleware de traitement** | Node-RED (localhost:1880) |
| **Base de données TSDB** | InfluxDB 3 Core v3.11.0 (localhost:8181) |
| **Outil de Tunneling** | ngrok v3.39.10 |
| **Dashboard de visualisation** | Grafana Cloud v13.2.0 |

### 4.2 Module d'acquisition (Firmware)
Le firmware, composé de 392 lignes de code C++ et représentant un exécutable compilé de 974 KB, est conçu de manière strictement non bloquante. La fonction `delay()` a été intégralement proscrite au profit de l'évaluation du temps écoulé via la fonction système `millis()`. Quatre tâches asynchrones sont définies avec des intervalles stricts : lecture des capteurs (1000ms), rafraîchissement de l'écran LCD (1000ms), affichage sur le port série (2000ms) et publication MQTT (3000ms). La synchronisation temporelle est assurée par un client NTP (pool.ntp.org configuré en UTC+1), avec un mécanisme de secours basé sur le compteur interne en cas de perte de réseau.

### 4.3 Implémentation du filtrage numérique
Afin d'atténuer le bruit des capteurs physiques, une moyenne glissante est implémentée dans le code. Les cinq dernières valeurs de chaque capteur sont conservées dans des tableaux circulaires (`tempBuffer[5]`).

```cpp
#define FILTER_SIZE 5
float tempBuffer[FILTER_SIZE];
int filterIndex = 0;

float applyMovingAverage(float newValue, float* buffer) {
    buffer[filterIndex] = newValue;
    float sum = 0.0;
    for (int i = 0; i < FILTER_SIZE; i++) {
        sum += buffer[i];
    }
    return sum / FILTER_SIZE;
}
```
Cette fonction est appelée à chaque cycle d'acquisition, l'indice `filterIndex` étant incrémenté circulairement modulo `FILTER_SIZE`.

### 4.4 Simulation de défauts et détection embarquée
Pour évaluer la réactivité du système, un simulateur de défaillance est intégré. La valeur du potentiomètre agit comme un facteur de dégradation mathématique. Si la consigne dépasse 50%, un coefficient `factor = (pot - 50) / 50.0` est calculé. Les variables physiques sont alors artificiellement altérées : la température augmente de `25 * factor`, la pression chute de `250 * factor`, l'altitude croît de `1500 * factor` et l'accélération subit un biais de `20 * factor`.

La détection d'anomalies s'effectue localement selon une logique de priorité stricte :
1. **Température critique :** Si `temp > 45°C`, le statut passe à "HIGH TEMP".
2. **Dépressurisation :** Si `pressure < 850 hPa`, le statut devient "LOW PRESSURE".
3. **Vibrations sévères :** Le vecteur accélération est calculé via la norme euclidienne `vibration = sqrt(ax² + ay² + (az - 9.8)²)` (en soustrayant la gravité terrestre). Si `vibration > 15 m/s²`, l'état indique "HIGH VIBRATION".
4. **Panne moteur majeure :** Si le potentiomètre dépasse 80%, le système déduit une "ENGINE FAILURE".

En présence de l'une de ces anomalies, le système passe en mode alerte : la LED verte s'éteint, la LED rouge s'illumine, le buzzer émet un signal strident à 1500 Hz, et l'écran LCD affiche immédiatement le motif d'alerte, en employant une technique de déduplication (comparaison de la variable `lastDisplay`) pour éviter les scintillements de l'écran.

### 4.5 Communication et formatage de la charge utile MQTT
La mise en réseau est gérée par des routines de reconnexion non bloquantes, tentant de rétablir la connexion Wi-Fi ou MQTT toutes les 5000 ms sans figer le programme principal. Pour garantir l'envoi de documents complets, la taille du buffer du client MQTT a été ajustée de manière préventive avec l'instruction `client.setBufferSize(512)`. 

Le payload JSON généré par l'ESP32 pèse environ 300 octets et inclut les métriques et les métadonnées de diagnostic :
```cpp
String payload = "{\"timestamp\":" + String(currentTimestamp) +
                 ",\"temperature\":" + String(filteredTemp) +
                 ",\"humidity\":" + String(filteredHum) +
                 ",\"pressure\":" + String(filteredPress) +
                 ",\"altitude\":" + String(filteredAlt) +
                 ",\"accX\":" + String(accX) +
                 ",\"accY\":" + String(accY) +
                 ",\"accZ\":" + String(accZ) +
                 ",\"potentiometer\":" + String(potValue) +
                 ",\"status\":\"" + currentStatus + "\"" +
                 ",\"reason\":\"" + alertReason + "\"}";
```
Ce message est publié sur le topic `aircraft/sensors` par le client `AircraftESP32-[MAC]`.

### 4.6 Middleware : Traitement sous Node-RED
Le flux (flow) Node-RED est l'épine dorsale du routage. Il débute par un nœud d'entrée MQTT souscrivant au topic cible avec l'identifiant de client `nodered-aircraft`. Le message traverse ensuite un nœud de fonction JavaScript `fn_parse_validate`. Ce script gère les cas critiques de corruption de données (JSON vide ou tronqué, données déjà désérialisées) et applique un horodatage de secours (fallback) si le module NTP de l'ESP32 est défaillant. 
Le flux se poursuit vers la fonction `fn_to_influx_points`, qui mappe les objets JSON en structures compatibles avec InfluxDB. Elle assigne la `measurement` ("sensors"), attribue les `tags` (ex: `device:ESP32`), insère les 8 champs (fields) numériques, et ajoute l'horodatage en millisecondes. Les données formatées sont enfin dirigées simultanément vers le nœud de sortie InfluxDB et un nœud de débogage.

[CAPTURE À INSÉRER : Flux Node-RED]

### 4.7 Stockage des séries temporelles (InfluxDB)
Les données sont ingérées dans un `bucket` InfluxDB nommé "aircraft", avec une `measurement` globale définie comme "sensors". L'architecture d'indexation repose fortement sur la notion de tags (comme `device=ESP32`), permettant à la base de partitionner efficacement les données pour des requêtes temporelles rapides.

### 4.8 Visualisation et tableau de bord (Grafana)
Le rendu visuel est assuré par Grafana Cloud, connecté à InfluxDB via la source de données configurée sous l'UID `atdh9j`. L'interface comprend 10 panneaux distincts disposés de manière ergonomique : quatre graphiques de séries temporelles (évolution de la température, de l'humidité, de la pression et de l'altitude), trois panneaux dédiés à l'accélération (axes X, Y, Z), une jauge analogique indiquant la position du potentiomètre de défaut, un indicateur d'état global (stat), et un tableau historique des dernières alertes. Le rafraîchissement global du dashboard est réglé sur un intervalle de 5 secondes pour garantir un suivi quasi-instantané.

[CAPTURE À INSÉRER : Dashboard Grafana complet]

### 4.9 Gestion des erreurs et logs
La résilience du système est assurée par une gestion granulaire des erreurs. Au niveau de l'ESP32, toutes les échecs de lecture de bus I2C ou de connexion réseau génèrent des traces (logs) explicites sur le port série à 115200 bauds. Côté serveur, les erreurs de syntaxe JSON identifiées par Node-RED sont capturées et archivées dans des fichiers de log locaux.

### 4.10 Résolution des problèmes techniques (D1 à D7)
Le développement de cette architecture complexe a été jalonné de nombreux obstacles techniques, dont la résolution itérative a permis de fiabiliser le système de bout en bout.

| Réf. | Problème technique rencontré | Diagnostic et Solution implémentée | Statut |
| :--- | :--- | :--- | :--- |
| **D1** | JSON vide ou corrompu dans Node-RED | Le flux réseau hachait parfois les trames. Implémentation d'une logique de validation JS robuste (Try/Catch) et gestion des objets partiellement parsés. | Résolu |
| **D2** | L'instruction `while(!Serial)` gèle Wokwi | Cette commande bloquante empêchait le simulateur de démarrer si le terminal virtuel n'était pas attaché. L'instruction a été supprimée purement. | Résolu |
| **D3** | Le BMP180 affichait 47750 Pa d'altitude erronée | La pression de référence par défaut était mal configurée. Correction manuelle du fichier `diagram.json` pour fixer la référence standard à 101325 Pa. | Résolu |
| **D4** | Incompatibilité du protocole gRPC au travers de ngrok | Le moteur InfluxDB 3 tentait de communiquer via gRPC, que le tunnel ngrok classique rejetait. Transition de la datasource vers le mode InfluxQL (HTTP/1.1 classique). | Résolu |
| **D5** | Erreur 401 (Non autorisé) sur le Token InfluxDB | Les paramètres d'en-tête du nœud Node-RED étaient mal formatés. Injection directe du jeton d'autorisation via les headers de l'API HTTP. | 95% finalisé |
| **D6** | Blocage réseau dû à ngrok v3.3.1 obsolète | Les connexions entrantes étaient refusées arbitrairement. Mise à jour critique du binaire de tunneling vers la version 3.39.10. | Résolu |
| **D7** | Déconnexions du Client MQTT pour cause de duplication | Plusieurs instances tentaient d'utiliser le même ID client statique. Modification du code pour inclure l'adresse MAC dynamique dans l'ID du client (`AircraftESP32-[MAC]`). | Résolu |

### 4.11 Tests unitaires et d'intégration
Une batterie de tests a été exécutée pour valider le comportement nominal de chaque composant de l'architecture.

**Tests du Firmware (6/6 Succès) :**
- Calcul de la moyenne glissante (`movingAverage`) : Validation de l'atténuation du bruit.
- Synchronisation NTP (`getTimestamp`) : Obtention de l'heure UTC+1 exacte.
- Acquisition I2C/GPIO (`readSensors`) : Lecture cohérente et sans blocage.
- Détection d'anomalies (`detectAnomaly`) : Respect strict des règles de priorité.
- Formatage JSON (`sendMQTT`) : Validation de la taille et de la syntaxe.
- Tolérance aux pannes réseau (`reconnectMQTT`) : Rétablissement en moins de 5 secondes.

**Tests API InfluxDB (5/5 Succès) :**
- Contrôle de santé (`health`).
- Authentification (`auth`).
- Moteur de requêtes relationnelles (`SQL`).
- Moteur de requêtes temporelles (`InfluxQL`).
- Injection de données via HTTP (`write`).

**Tests du Tunnel ngrok (3/3 Succès) :**
- Accessibilité (`ping`).
- Routage du trafic `SQL` et `InfluxQL`.

**Test d'intégration Grafana :**
L'outil de diagnostic intégré à Grafana a confirmé la validité de l'architecture de bout en bout en retournant le statut : *"datasource is working. 1 measurements found"*, validant ainsi le requêtage de la base de données distante.

### 4.12 Validation fonctionnelle par scénarios de test
L'ultime étape de validation a consisté à simuler l'évolution physiologique du système via l'injection contrôlée de défauts par le potentiomètre. Ces scénarios confirment que les règles métiers sont correctement évaluées, transmises et affichées.

| Scénario de test | Action (Potentiomètre) | Valeur Physique induite | Résultat observé (Firmware & Cloud) | Statut |
| :--- | :--- | :--- | :--- | :--- |
| **Nominal** | Réglé à 0% | Valeurs ambiantes normales | Système au vert, transmission OK, Statut : **NORMAL** | ✅ |
| **Surchauffe** | Montée à 95% | Température atteint 47.5°C | Déclenchement alarme de niveau 1, Statut : **ALERT HIGH TEMP** | ✅ |
| **Dépressurisation** | Descente à 85% | Pression chute à 838 hPa | Alarme de baisse de pression, Statut : **ALERT LOW PRESSURE** | ✅ |
| **Vibration critique** | Réglé à 80% | Accélération atteint 17 m/s² | Alarme de chocs/vibrations, Statut : **ALERT HIGH VIBRATION** | ✅ |
| **Panne moteur** | Montée à 90% | (Combinaison de facteurs) | Déclenchement de l'erreur fatale, Statut : **ALERT ENGINE FAILURE** | ✅ |

### Conclusion du chapitre
Ce quatrième chapitre a dressé un bilan complet et technique du travail d'implémentation accompli. Grâce à un choix d'outils rigoureux et à une méthodologie itérative efficace, tous les sous-systèmes — de l'acquisition matérielle à la visualisation en passant par le traitement réseau — ont été codés, interfacés et éprouvés. Les défis techniques rencontrés ont trouvé des solutions solides, aboutissant à une architecture IoT à cinq couches stable, réactive et apte à supporter des opérations de maintenance prédictive aéronautique en temps réel.
