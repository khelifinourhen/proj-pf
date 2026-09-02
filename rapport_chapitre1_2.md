# CHAPITRE 1 — CONTEXTE GÉNÉRAL, ÉTUDE DE L'EXISTANT ET CAHIER DES CHARGES

**Plan du chapitre :**
* Introduction
* 1.1 Présentation de l'organisme d'accueil
* 1.2 Contexte général du projet
* 1.3 Problématique
* 1.4 Étude et critique de l'existant
* 1.5 Cahier des charges
* 1.6 Méthodologie de travail
* 1.7 Planification du projet
* Conclusion

## Introduction
Le présent chapitre introduit le cadre général dans lequel s'inscrit ce Projet de Fin d'Études (PFE). Il débute par une présentation de l'organisme d'accueil, suivie de la mise en évidence du contexte global et de la problématique inhérente à la surveillance des paramètres critiques dans le domaine aéronautique. Par la suite, une étude critique des solutions existantes est menée afin de justifier les orientations prises. Enfin, le cahier des charges, la méthodologie de gestion de projet adoptée et la planification prévisionnelle sont détaillés pour délimiter rigoureusement le périmètre de l'étude.

## 1.1 Présentation de l'organisme d'accueil
Ce projet a été réalisé au cours d'un stage d'été 2026 au sein de l'entreprise **YaneCode Digital**. YaneCode Digital est une structure spécialisée dans les domaines de pointe, notamment l'Aéronautique (Aeronautics) et les Systèmes Embarqués (Embedded Systems). L'entreprise s'illustre par son expertise dans le développement de solutions numériques innovantes alliant l'Internet des Objets (IoT), le traitement de données en temps réel et l'intelligence artificielle pour répondre aux exigences industrielles strictes.

**Organigramme de l'entreprise :**
[À COMPLÉTER] : L'organigramme de YaneCode Digital reflète une structure agile et pluridisciplinaire.

*Figure 1.1 : Organigramme de YaneCode Digital* [FIGURE À AJOUTER]

## 1.2 Contexte général du projet
Dans le secteur de l'aéronautique, la fiabilité et la sécurité des systèmes reposent sur une surveillance continue et rigoureuse des paramètres environnementaux et structurels. L'avènement de l'Internet des Objets (IoT) et des systèmes embarqués a révolutionné ces processus en permettant une télémétrie omniprésente et à faible coût. L'intégration de capteurs intelligents sur les aéronefs, drones ou équipements au sol permet de remonter des données cruciales en temps réel. Le besoin de surveillance s'accentue avec la complexification des missions et la nécessité d'anticiper les défaillances (maintenance prédictive) pour garantir la sécurité des vols et optimiser la durée de vie des équipements.

## 1.3 Problématique
Malgré les avancées technologiques, la surveillance des paramètres critiques aéronautiques fait face à plusieurs défis majeurs :
* Comment garantir l'acquisition fiable, le filtrage et la transmission en temps réel de données hétérogènes (température, pression, altitude, vibrations) dans un environnement contraint ?
* De quelle manière peut-on détecter instantanément, au niveau du nœud (Edge), une anomalie potentiellement critique (ex: défaillance moteur) avant même que la donnée ne soit transmise au cloud ?
* Comment structurer une architecture IoT complète (du capteur à la visualisation) qui soit à la fois modulaire, évolutive et adaptée aux normes de réactivité aéronautique ?

## 1.4 Étude et critique de l'existant

### 1.4.1 Analyse des solutions existantes de monitoring
La majorité des solutions de monitoring industriel traditionnelles reposent sur des architectures SCADA centralisées, souvent coûteuses, propriétaires et peu adaptées au déploiement rapide sur des flottes de drones ou des systèmes légers. Les systèmes basés sur le cloud exclusif souffrent parfois de latence et d'une dépendance totale à la connectivité.

### 1.4.2 Analyse des architectures embarquées existantes
Les architectures embarquées actuelles utilisent couramment des microcontrôleurs classiques (type Arduino) qui manquent de capacités de communication natives (WiFi/Bluetooth) et de puissance de calcul pour intégrer des règles de détection locales complexes. À l'inverse, des systèmes de type Raspberry Pi offrent une puissance importante mais consomment trop d'énergie et ne répondent pas toujours aux contraintes temps réel strictes des systèmes d'exploitation embarqués (RTOS).

### 1.4.3 Critique de l'existant
L'existant présente un compromis difficile entre coût, consommation énergétique, capacités de communication et intelligence locale. Il manque souvent une approche hybride où le traitement critique est effectué en Edge (proche du capteur) tandis que l'historisation et l'analyse lourde sont déportées vers des plateformes Cloud modernes et open-source.

## 1.5 Cahier des charges

### 1.5.1 Objectifs du projet
Le projet vise à concevoir et simuler une solution IoT embarquée de bout en bout pour la surveillance des paramètres aéronautiques critiques. Il s'agit de mettre en place une chaîne complète : acquisition de données, traitement local avec détection d'anomalies, communication sans fil, stockage optimisé et visualisation via un tableau de bord dynamique.

### 1.5.2 Périmètre fonctionnel
* **Acquisition :** Lecture des données de température, humidité, pression, altitude, vibrations et état de la motorisation (simulé par potentiomètre).
* **Traitement Edge :** Filtrage des données et détection de seuils critiques (ex: ENGINE FAILURE).
* **Signalisation locale :** Affichage sur écran LCD I2C, et alertes via LED (Verte/Rouge) et Buzzer.
* **Transmission :** Envoi des données via le protocole MQTT vers un broker public.
* **Intégration et Visualisation :** Routage via Node-RED, stockage dans une base de données temporelle, et affichage sur 10 panneaux de contrôle rafraîchis toutes les 5 secondes.

### 1.5.3 Contraintes techniques
* Simulation intégrale de la composante matérielle via l'environnement Wokwi.
* Utilisation d'un microcontrôleur intégrant la connectivité réseau (ESP32).
* Latence de transmission et de rafraîchissement réduite au minimum.
* Fiabilité des seuils de déclenchement d'alerte sur la carte embarquée.

### 1.5.4 Critères de validation
Le système sera jugé valide si :
* Les données simulées sont acquises sans perte et filtrées correctement.
* Une anomalie déclenche instantanément le Buzzer et la LED Rouge sur l'ESP32.
* Les données atteignent la base de données temporelle avec l'horodatage correct.
* Le tableau de bord affiche les variations en temps réel avec un délai maximum de 5 secondes.

## 1.6 Méthodologie de travail
Pour mener à bien ce projet, la méthode agile **Kanban** a été adoptée. Elle offre une gestion visuelle du flux de travail, permettant d'identifier rapidement les goulots d'étranglement et de s'adapter aux changements de spécifications. Les tâches ont été divisées en colonnes classiques (À faire, En cours, En test, Terminé), assurant un suivi continu et une livraison incrémentale des modules (Hardware, Software embarqué, Backend, Frontend).

## 1.7 Planification du projet
La répartition des tâches et le calendrier du projet ont été modélisés à l'aide d'un diagramme de Gantt, couvrant l'ensemble de la période du stage estival.

*Figure 1.2 : Diagramme de Gantt du projet* [FIGURE À AJOUTER]

## Conclusion
Ce premier chapitre a posé les fondations du projet en présentant YaneCode Digital et en définissant le contexte aéronautique. L'identification de la problématique et la critique des systèmes existants ont conduit à l'élaboration d'un cahier des charges précis, définissant les objectifs et les contraintes de notre solution IoT. La méthodologie Kanban retenue garantira la bonne exécution des tâches. Le chapitre suivant s'attachera à explorer l'état de l'art et à justifier de manière scientifique et technique les choix matériels et logiciels qui composeront notre architecture.

---

# CHAPITRE 2 — ÉTAT DE L'ART ET JUSTIFICATION DES CHOIX TECHNOLOGIQUES

**Plan du chapitre :**
* Introduction
* 2.1 Systèmes IoT et architectures embarquées pour le monitoring
* 2.2 Cartes embarquées et plateformes de traitement
* 2.3 Capteurs et paramètres critiques aéronautiques
* 2.4 Acquisition et prétraitement des données
* 2.5 Détection d'anomalies et IA en Edge
* 2.6 Protocoles de communication IoT
* 2.7 Solutions de stockage et de visualisation
* Conclusion

## Introduction
La conception d'une architecture IoT performante pour le secteur aéronautique requiert une sélection minutieuse des composants matériels et logiciels. Ce chapitre propose un état de l'art détaillé des technologies employées dans les systèmes embarqués modernes. Une étude comparative est menée à chaque étape critique du flux de données (du capteur jusqu'au cloud) afin de justifier rigoureusement les choix adoptés pour notre solution de surveillance, en adéquation avec les exigences du cahier des charges.

## 2.1 Systèmes IoT et architectures embarquées pour le monitoring
Une architecture IoT standard pour le monitoring industriel se divise généralement en trois couches : la couche de perception (capteurs et actionneurs), la couche réseau (protocoles de communication et passerelles), et la couche application (stockage, analyse et visualisation). Dans un contexte critique, il est primordial de décentraliser une partie de l'intelligence vers la couche de perception, concept connu sous le nom d'Edge Computing, afin d'assurer une réactivité immédiate face aux défaillances.

## 2.2 Cartes embarquées et plateformes de traitement

### 2.2.1 ESP32
Le microcontrôleur ESP32 (DevKit C v4) d'Espressif Systems est une puce SoC (System on a Chip) très prisée en IoT. Il dispose d'un processeur dual-core cadencé à 240 MHz, de 520 KB de RAM, et intègre nativement des modules WiFi et Bluetooth (BLE). Son coût abordable (environ 5€) et son intégration native dans des simulateurs comme Wokwi en font un candidat de choix.

### 2.2.2 STM32
La famille STM32 (STMicroelectronics) est basée sur des cœurs ARM Cortex-M. Elle offre une robustesse industrielle, une grande variété de périphériques et une consommation maîtrisée. Cependant, la connectivité sans fil n'est généralement pas intégrée nativement sur les modèles d'entrée/milieu de gamme, nécessitant l'ajout de modules externes.

### 2.2.3 Raspberry Pi
Les nano-ordinateurs Raspberry Pi (ex: Zero ou 4) offrent des capacités de traitement proches d'un ordinateur classique avec des systèmes d'exploitation basés sur Linux. Ils sont idéaux pour des algorithmes lourds mais leur consommation électrique, leur temps de démarrage et leur absence de déterminisme temps réel strict les rendent moins adaptés pour un nœud de capteur embarqué bas niveau.

### 2.2.4 Comparaison

*Tableau 2.1 : Comparaison des plateformes embarquées*

| Caractéristique | ESP32 | Arduino Uno | Raspberry Pi Zero W | STM32 (F4) |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Xtensa Dual-core 32-bit | AVR 8-bit | ARM11 32-bit | ARM Cortex-M4 32-bit |
| **Fréquence** | 240 MHz | 16 MHz | 1 GHz | 84 - 180 MHz |
| **RAM** | 520 KB | 2 KB | 512 MB | Jusqu'à 384 KB |
| **Connectivité native**| WiFi, Bluetooth | Aucune | WiFi, Bluetooth | Dépend du modèle (rare)|
| **Consommation** | Moyenne (modes veille) | Faible | Élevée | Très faible |
| **Coût approximatif**| ~5 € | ~20 € | ~15 € (si disponible) | ~10-15 € |

*Interprétation :* Le Tableau 2.1 met en évidence le compromis exceptionnel offert par l'ESP32, alliant une forte puissance de calcul, une connectivité réseau native et un coût minime par rapport à ses concurrents.

### 2.2.5 Justification du choix
Le choix s'est porté sur l'**ESP32 DevKit C v4**. Sa connectivité WiFi intégrée est indispensable pour la publication MQTT. Son processeur dual-core offre la puissance nécessaire pour acquérir simultanément plusieurs capteurs (I2C, Analogique, Numérique) tout en exécutant des règles de détection d'anomalies (Edge Computing). Enfin, sa simulation parfaite sur la plateforme Wokwi répond à la contrainte de virtualisation du projet.

## 2.3 Capteurs et paramètres critiques aéronautiques

L'acquisition de paramètres d'environnement et de mouvement est assurée par trois capteurs principaux, complétés par un potentiomètre simulant la puissance moteur.

### 2.3.1 Température et Humidité (DHT22)
Le DHT22 (câblé sur le GPIO15) est un capteur numérique mesurant l'humidité relative (0-100% RH) et la température (-40°C à +80°C) avec une précision de ±0.5°C. Ces paramètres préviennent les risques de givrage ou de surchauffe des équipements.

### 2.3.2 Pression et Altitude (BMP180)
Le capteur barométrique BMP180 communique via le bus I2C (adresse 0x77). Il mesure la pression absolue (en hPa) et permet d'estimer l'altitude relative en utilisant la pression atmosphérique standard au niveau de la mer (1013.25 hPa) comme référence. La surveillance de l'altitude et de la dépressurisation est vitale en aéronautique.

### 2.3.3 Vibration et mouvement (MPU6050)
Le MPU6050 intègre un accéléromètre 3 axes et un gyroscope 3 axes (I2C, adresse 0x68). Dans ce projet, nous utilisons l'accéléromètre pour mesurer les vibrations (AccX, AccY, AccZ) en m/s². Des vibrations excessives sont le signe précurseur de défaillances mécaniques ou structurelles.

### 2.3.4 Comparaison des capteurs
Le choix de ces composants s'inscrit dans un standard éducatif et de prototypage industriel rapide, offrant une interface de communication standardisée (I2C, GPIO numérique).

### 2.3.5 Justification
Les capteurs DHT22, BMP180 et MPU6050 ont été choisis pour leur haute disponibilité dans les environnements de simulation, leur excellente documentation et leur adéquation avec les paramètres critiques (thermiques, atmosphériques, dynamiques) ciblés par la surveillance des aéronefs.

## 2.4 Acquisition et prétraitement des données
Pour garantir la qualité des données remontées, un filtrage local est appliqué aux signaux bruts, particulièrement sujets au bruit (notamment l'accéléromètre). Un filtre de moyenne mobile (Moving Average Filter) a été implémenté sur l'ESP32 avec une taille de fenêtre (FILTER_SIZE) de 5. L'équation de filtrage s'exprime par :

$$ y[n] = \frac{1}{N} \sum_{i=0}^{N-1} x[n-i] $$

où $y[n]$ est la valeur filtrée, $x[n-i]$ sont les valeurs acquises précédemment, et $N=5$. Ce lissage évite les déclenchements de fausses alertes dues à des pics de mesure aberrants.

## 2.5 Détection d'anomalies et IA en Edge

### 2.5.1 Approche par Seuils (Threshold-based)
La méthode première mise en œuvre sur l'ESP32 est déterministe, basée sur des seuils de criticité :
* Température > 45°C
* Pression < 850 hPa
* Vibrations > 15 m/s²
* Potentiomètre > 80% (Simulant un emballement ou une défaillance moteur "ENGINE FAILURE")
Le dépassement de l'un de ces seuils active instantanément l'actionneur d'alerte locale (Buzzer sur GPIO25 et LED Rouge sur GPIO27), garantissant une réactivité temps réel absolue, indépendante de la latence réseau.

### 2.5.2 Méthodes de Machine Learning étudiées
Afin d'envisager une détection d'anomalies plus complexe (anomalies contextuelles ou dérives lentes), plusieurs modèles ont été étudiés théoriquement pour une potentielle implémentation Cloud ou Edge ML :
* **Isolation Forest :** Efficace pour séparer les anomalies des données normales dans un espace multidimensionnel, adapté aux jeux de données massifs.
* **One-Class SVM :** Modélise le comportement normal et détecte toute déviation, utile lorsque seules des données de vol "normales" sont disponibles à l'entraînement.
* **Autoencoder LSTM :** Réseaux de neurones profonds excellant dans la détection d'anomalies sur des séries temporelles séquentielles (Time Series).

### 2.5.3 Comparaison des méthodes d'IA et Datasets
Ces modèles ont été mis en perspective en étudiant les bases de données *SurveilDrone-Net23* (comportant plus de 140 256 enregistrements de vol de drones) et *NASA SMAP/MSL Telemanom* (données de télémétrie spatiale). L'Autoencoder LSTM montre une précision supérieure sur les séries temporelles, mais nécessite des ressources de calcul élevées, incompatibles avec un ESP32 sans optimisation drastique (quantification TensorFlow Lite).

### 2.5.4 Justification
Pour la réalisation pratique de ce PFE, l'approche par seuils statiques embarqués a été justifiée et implémentée car elle garantit le déterminisme, consomme très peu de ressources CPU/RAM et répond au besoin de réactivité instantanée pour des alertes critiques telles que la panne moteur.

## 2.6 Protocoles de communication IoT

### 2.6.1 Comparaison des protocoles (WiFi, Bluetooth, UART, MQTT)
Dans l'IoT, la transmission d'informations nécessite un protocole léger. L'UART et le Bluetooth (BLE) sont limités par leur portée physique. Pour la transmission réseau, des protocoles applicatifs tels que HTTP, WebSocket, CoAP et MQTT s'affrontent.

*Tableau 2.2 : Comparaison des protocoles applicatifs IoT*

| Caractéristique | MQTT | HTTP/REST | CoAP | WebSocket |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Publish/Subscribe | Request/Response | Request/Response | Full-duplex |
| **Overhead (En-tête)**| 2 octets (min) | Très lourd | Léger (~4 octets) | Moyen |
| **QoS (Qualité de Service)**| Oui (0, 1, 2) | Non | Non | Non |
| **Maintien de connexion**| Automatique, robuste | Non (stateless) | UDP (non fiable) | Connexion persistante|

*Interprétation :* Le Tableau 2.2 démontre la supériorité de MQTT pour les environnements IoT contraints. Son architecture de publication/souscription et son en-tête réduit à 2 octets minimisent la bande passante.

### 2.6.2 Justification du choix MQTT
Le protocole **MQTT** a été retenu. L'ESP32 publie les trames JSON sur le topic `aircraft/sensors` via le broker public `broker.hivemq.com` sur le port 1883. Ce choix assure un couplage lâche, une reconnexion automatique et une scalabilité optimale si l'on souhaitait ajouter des centaines de capteurs simultanément.

## 2.7 Solutions de stockage et de visualisation

Pour exploiter les données MQTT, un middleware (Node-RED) est utilisé pour router l'information vers la base de données, suivie d'un outil de visualisation.

* **Bases de données temporelles :** InfluxDB 3, TimescaleDB, Prometheus, SQLite.
* **Outils de visualisation :** Grafana, Kibana, Tableau, Power BI.
* **Simulateurs matériels :** Wokwi, Proteus, SimulIDE, TinkerCAD.

*Tableau 2.3 : Sélection de l'écosystème logiciel*

| Composant | Solution Choisie | Justification |
| :--- | :--- | :--- |
| **Simulateur** | **Wokwi** | Support natif et gratuit de l'ESP32, simulation WiFi réelle, partage de projets simplifié par rapport à Proteus ou TinkerCAD (limité à Arduino). |
| **Routage** | **Node-RED** | Programmation visuelle, nœuds MQTT in/out natifs, intégration facile avec les bases de données. |
| **Stockage** | **InfluxDB 3 Core v3.11.0** | Conçu spécifiquement pour les séries temporelles (Time Series). Création d'un bucket `aircraft` et d'une mesure `sensors`. Excellente compression par rapport à SQLite. |
| **Visualisation** | **Grafana Cloud** | Création d'un dashboard de 10 panneaux de contrôle. Intégration native avec InfluxDB, rafraîchissement performant configuré à 5 secondes, alertes visuelles personnalisables. |

## Conclusion
Ce chapitre a permis d'explorer l'état de l'art des composants entrant dans la chaîne de valeur IoT et d'argumenter nos choix technologiques. L'architecture globale retenue s'articule autour d'un ESP32 simulé sous Wokwi, effectuant une acquisition lissée par moyenne mobile et une détection d'anomalies par seuils. La remontée des données est assurée par le protocole léger MQTT vers un broker HiveMQ, avant d'être orchestrée par Node-RED, stockée efficacement dans InfluxDB 3 et restituée dynamiquement sur Grafana. Le chapitre suivant sera consacré à la mise en œuvre pratique et au déploiement de ces différentes briques logicielles.
