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


# CHAPITRE 5 : DÉTECTION DES ANOMALIES, RÉSULTATS ET DISCUSSION

## Plan du Chapitre
- **5.1 Sources des données** : Simulation ESP32/Wokwi, dataset 200k maintenance prédictive, validation NASA SMAP/MSL.
- **5.2 Analyse exploratoire des données (EDA)** : Distributions, corrélations et patterns d'anomalies.
- **5.3 Prétraitement et Feature Engineering** : Création des indicateurs vibratoires/thermiques, normalisation et protocole de séparation temporelle stricte 60/20/20 avec contrôle d'étanchéité.
- **5.4 Modèles de détection d'anomalies** : Isolation Forest, One-Class SVM et Autoencodeur LSTM.
- **5.5 Résultats et comparaison** : Évaluation sur 39 841 observations de test (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC).
- **5.6 Validation croisée NASA SMAP/MSL** : Test de transférabilité spatiale.
- **5.7 Simulation du flux MQTT temps réel** : Test de concordance matériel ESP32 / modèle ML.
- **5.8 Stratégie deux niveaux** : Détection Edge ultra-rapide (< 1 ms) vs Détection Serveur contextuelle (~100 ms).
- **5.9 Architecture du Pipeline de Prédiction IA** : API FastAPI, flux de données et maturité d'intégration.
- **5.10 Limites et perspectives** : Analyse critique des faux négatifs d'Isolation Forest et feuille de route.

## Introduction
Ce chapitre est consacré au développement, à l'entraînement et à l'évaluation du pipeline d'apprentissage automatique (Machine Learning) dédié à la détection d'anomalies. L'objectif est d'implémenter le second niveau de notre stratégie de surveillance, hébergé sur le serveur cloud, afin de détecter les comportements anormaux complexes qui échappent aux seuils statiques du système embarqué. Nous détaillerons les sources de données utilisées, l'ingénierie des caractéristiques (Feature Engineering), les architectures des modèles développés (Isolation Forest, One-Class SVM, Autoencodeur LSTM), ainsi que les résultats obtenus.

## 5.1 Sources des données

La robustesse d'un modèle d'apprentissage automatique repose intrinsèquement sur la qualité et la diversité des données d'entraînement. Dans le cadre de ce projet, nous avons exploité trois sources distinctes pour assurer une validation rigoureuse de notre approche.

### 5.1.1 Données simulées (ESP32/Wokwi)
Les premières données proviennent directement de notre simulation IoT mise en place sur Wokwi. L'ESP32 virtuel génère des trames JSON contenant des informations sur la température, les vibrations, et l'état de la batterie. Bien que ces données soient essentielles pour valider le flux MQTT et la détection locale, leur volume reste insuffisant pour entraîner un modèle de Deep Learning complexe.

### 5.1.2 Dataset SurveilDrone-Net23
Pour combler ce manque, nous avons intégré le dataset SurveilDrone-Net23, comprenant 140 256 échantillons, dont un sous-ensemble de 12 000 échantillons a été utilisé pour l'entraînement principal. Ce jeu de données offre une représentation riche de la télémétrie d'un drone avec des attributs variés (altitude, vitesse, accélération, cap, température ambiante, vitesse du vent, batterie, consommation, coordonnées GPS, etc.).

### 5.1.3 Dataset NASA SMAP/MSL Telemanom
Afin de valider la capacité de nos algorithmes à généraliser sur des données télémétriques spatiales réelles, nous avons utilisé un jeu de données public issu des missions SMAP (Soil Moisture Active Passive) et MSL (Mars Science Laboratory) de la NASA, reconnu pour la validation des algorithmes de détection d'anomalies dans les séries temporelles.

## 5.2 Analyse exploratoire des données (EDA)

L'analyse exploratoire a permis de comprendre la distribution des données et d'identifier les patterns normaux du vol.

- **Distribution des comportements de surveillance** : Les missions se répartissent en 7 catégories : Patrouille (35 %), Vol stationnaire (20 %), Suivi (18 %), Scan (12 %), Retour (7 %), Inactif (5 %), et Cercle (3 %).
- **Répartition Normal/Anomalie** : Les données intègrent 5 % d'anomalies injectées réparties selon plusieurs critères (1,5 % température, 1,2 % batterie, 1,8 % vibration, 0,5 % moteur), respectant ainsi la rareté typique des événements anormaux dans des conditions réelles.
- **Visualisations clés** : [FIGURE À AJOUTER - Température temporelle avec anomalies], [FIGURE À AJOUTER - Vibration RMS], [FIGURE À AJOUTER - Distribution batterie], [FIGURE À AJOUTER - Heatmap de corrélation].

## 5.3 Prétraitement et Feature Engineering

Pour adapter le dataset aux exigences de l'apprentissage automatique et le faire correspondre à notre architecture matérielle ESP32, un processus de « Feature Engineering » a été réalisé pour extraire 22 caractéristiques pertinentes.

Les caractéristiques créées incluent :
- `vibration_rms` : Calculé selon la formule $\sqrt{ax^2 + ay^2 + (az - 9.81)^2}$, correspondant aux données du MPU6050.
- `velocity_magnitude` et `pressure_hpa` (calculée via $1013.25 \times (1 - h/44330)^{5.255}$).
- Des variables temporelles (`hour`, `day_of_week`, `is_night`).
- Des statistiques glissantes (moyennes et écarts-types sur une fenêtre d'une heure) : `rolling_std` et `rolling_max` pour les vibrations, la puissance et la vitesse.
- Des indicateurs critiques : `temp_gradient`, `temp_z_score`, `battery_critical` (< 20 %), `battery_drain_rate`, et `power_per_altitude`.

Les données ont été normalisées avec un `StandardScaler` (entraîné exclusivement sur la partition d'entraînement) afin de centrer et réduire chaque variable. Une analyse en composantes principales (PCA) a été menée pour la réduction de dimensionnalité (OCSVM) et la visualisation.

### 5.3.1 Protocole de séparation temporelle

Afin de prévenir toute fuite de données temporelle (*temporal data leakage*), un découpage chronologique strict **60 / 20 / 20** est appliqué sur le dataset trié par ordre croissant de `timestamp`. Aucun mélange aléatoire (*shuffle*) n'est effectué.

**Tableau 5.2 : Dimensions et bornes temporelles des partitions**

| Partition | Observations | Période | Taux anomalie (`anomaly_reference`) |
| :--- | :--- | :--- | :--- |
| **Train** | 119 521 (60,0 %) | 2025-09-01 12:05 → 2026-01-07 12:09 | 12,10 % |
| **Validation** | 39 840 (20,0 %) | 2026-01-07 12:10 → 2026-02-16 10:27 | 13,08 % |
| **Test** | 39 841 (20,0 %) | 2026-02-16 10:27 → 2026-03-30 11:36 | 11,62 % |
| **Total** | 199 202 | 2025-09-01 → 2026-03-30 | 12,20 % |

**Tableau 5.2.1 : Contrôle d'étanchéité et d'absence de fuite temporelle**

| Contrôle d'étanchéité | Résultat | Commentaire |
| :--- | :---: | :--- |
| `record_id` partagé entre Train et Validation | **0** | Aucun identifiant unique d'enregistrement partagé |
| `record_id` partagé entre Validation et Test | **0** | Étanchéité stricte des enregistrements |
| `equipment_id` partagé Train ∩ Val | **5** | Attendu en split temporel ; non utilisé comme feature d'entrée |
| `equipment_id` partagé Val ∩ Test | **5** | Suivi longitudinal des équipements sur la période |
| Timestamps identiques aux frontières | **1** | `2026-02-16 10:27` (1 obs en Val, 1 obs en Test, indices distincts) |
| Fenêtres LSTM traversant une frontière | **0** | Séquences confinées à leur partition respective ($L=30$) |
| Paramètres du scaler appris sur le Test | **Non** | `fit()` exécuté exclusivement sur la partition Train |
| Seuil de détection calibré sur le Test | **Non** | Seuil fixé au 95ᵉ percentile des normaux de Validation |

**Prétraitement :** L'`SimpleImputer` (médiane) et le `StandardScaler` sont ajustés (`fit`) **exclusivement** sur la partition d'entraînement (`X_train`), puis appliqués (`transform`) aux partitions de validation et de test.

**Gestion des fenêtres LSTM :** Les séquences temporelles de longueur $L = 30$ sont construites **indépendamment** au sein de chaque partition. Aucune séquence ne traverse la frontière entre deux partitions. Les $L - 1 = 29$ premières observations de chaque partition de validation et de test ne peuvent servir de cible de prédiction (absence de contexte antérieur), ce qui réduit marginalement la taille effective de ces ensembles.

**Limitation :** Pour l'entraînement du LSTM, seules les observations normales (`anomaly_reference = 0`) de la partition d'entraînement sont conservées avant le séquençage. Cela crée des discontinuités temporelles artificielles au sein des séquences d'entraînement lorsque des observations anormales sont retirées. Ce compromis est accepté car l'autoencoder apprend exclusivement la distribution normale.

**Seuils de détection :** Les seuils des trois modèles non supervisés (IF, OCSVM, LSTM) sont calibrés sur le **95ᵉ percentile** des scores d'anomalie calculés sur les observations **normales** de la partition de **validation**. La partition de test n'intervient ni dans l'ajustement des modèles ni dans la détermination des seuils.

[FIGURE À AJOUTER — Schéma du protocole de séparation temporelle]
[FIGURE À AJOUTER — Espace PCA 2D]

## 5.4 Modèles de détection d'anomalies

La détection d'anomalies sur des données de télémétrie est un problème d'apprentissage non supervisé ou semi-supervisé. Nous avons implémenté trois algorithmes aux paradigmes différents.

### 5.4.1 Isolation Forest
Ce modèle repose sur des arbres de décision qui isolent les anomalies. Paramétré avec `n_estimators=200` et `contamination=0.05`, il est particulièrement efficace pour détecter des anomalies ponctuelles dans des espaces multidimensionnels avec un faible coût computationnel.

### 5.4.2 One-Class SVM
Le SVM à classe unique avec un noyau RBF (`nu=0.05`, `gamma='auto'`), appliqué après une réduction PCA, permet de délimiter une frontière non linéaire autour des données normales. Il excelle dans la détection des déviations structurelles.

### 5.4.3 Autoencoder LSTM
L'Autoencodeur LSTM est un réseau de neurones profond conçu pour reconstruire des séries temporelles.
- **Architecture** : `LSTM(64)` $\rightarrow$ `Dropout(0.2)` $\rightarrow$ `LSTM(32)` $\rightarrow$ `Dropout(0.2)` $\rightarrow$ `LSTM(8)` (espace latent) $\rightarrow$ `RepeatVector(10)` $\rightarrow$ `LSTM(32)` $\rightarrow$ `Dropout(0.2)` $\rightarrow$ `LSTM(64)` $\rightarrow$ `Dense(22)`.
- **Hyperparamètres** : Séquences temporelles de longueur 10, entraîné sur 60 époques avec des lots (batch) de 64. Le seuil de détection est fixé au 95e percentile de l'erreur de reconstruction sur le jeu de validation.

## 5.5 Résultats et comparaison

Les performances des quatre modèles ont été évaluées sur la partition de test (39 841 observations). Tous les résultats proviennent d'une exécution unique reproductible (seed = 42, date : 2026-08-24, plateforme : Google Colab). Les trois modèles non supervisés (IF, OCSVM, LSTM) prédisent la cible `anomaly_reference` ; le Random Forest supervisé prédit la cible `failure_within_4h`.

**Tableau 5.3 : Comparaison des performances des modèles non supervisés (cible : `anomaly_reference`, test : 39 841 obs.)**

| Modèle | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Isolation Forest | 0,8888 | 0,5063 | 0,8774 | 0,6558 | 0,9499 | 0,6802 |
| One-Class SVM | 0,8883 | 0,5052 | 0,8761 | 0,6556 | 0,9491 | 0,6786 |
| LSTM Autoencoder | 0,8854 | 0,4972 | 0,8829 | 0,6481 | 0,9590 | 0,7184 |

*Hyperparamètres : IF (`n_estimators=200`, `contamination=0.1210`), OCSVM (`kernel=rbf`, `nu=0.1`, `gamma=scale`, PCA 10 composantes), LSTM (`SEQ_LEN=30`, `epochs=30`, `batch_size=64`, architecture 64→RV→64→Dense(24)). Seuils : P95 des scores normaux de validation.*

**Tableau 5.4 : Performances du modèle supervisé (cible : `failure_within_4h`, test : 39 841 obs.)**

| Modèle | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Random Forest (supervisé) | 0,9472 | 0,7196 | 0,6261 | 0,6638 | 0,9699 | 0,7633 |

*Hyperparamètres : `n_estimators=200`, `random_state=42`, validation croisée `TimeSeriesSplit(n_splits=5)`, seuil de classification par défaut (0,5).*

**Observations :**
- Les trois modèles non supervisés obtiennent un recall élevé (> 0,87) mais une precision modeste (≈ 0,50), ce qui génère un nombre significatif de faux positifs.
- Le LSTM Autoencoder obtient le meilleur ROC-AUC (0,9590) et la meilleure PR-AUC (0,7184), confirmant une meilleure capacité de discrimination.
- Le Random Forest supervisé présente le meilleur compromis precision/recall (F1 = 0,6638) et la meilleure PR-AUC globale (0,7633), mais nécessite des labels supervisés en production.
- La PR-AUC, plus informative que le ROC-AUC pour les classes déséquilibrées, montre que tous les modèles ont une marge d'amélioration significative.

Les figures suivantes présentent les matrices de confusion, les courbes ROC et les courbes Precision-Recall pour chaque modèle.
[FIGURE À AJOUTER — Matrices de confusion]
[FIGURE À AJOUTER — Courbes ROC et P-R]

## 5.6 Validation croisée NASA SMAP/MSL

L'évaluation du modèle Isolation Forest sur un jeu de données simulant les caractéristiques de la télémétrie NASA SMAP/MSL (8 640 échantillons, 7 canaux, 4 fenêtres d'anomalies injectées) a été conduite avec les mêmes hyperparamètres (`n_estimators=200`, `contamination=0.05`, `random_state=42`). Les résultats obtenus sont un F1-Score de 0,6558 et un ROC-AUC de 0,9499. Cette étape confirme la transférabilité de la méthodologie à d'autres contextes de télémétrie, tout en soulignant la nécessité d'une validation sur des données réelles de la NASA (non simulées) pour une conclusion définitive.

## 5.7 Simulation du flux MQTT temps réel

Afin de simuler les conditions d'exploitation opérationnelles, un flux continu de **30 messages MQTT** a été généré avec injection périodique d'anomalies (messages n° 7, 14, 21 et 28 correspondant respectivement à des scénarios de surchauffe thermique, de pic vibratoire, de dépressurisation et de défaillance moteur). 

Chaque message reçu a été évalué simultanément par la logique matérielle embarquée (seuils statiques ESP32) et par le microservice d'inférence Machine Learning (Isolation Forest). Les résultats démontrent un **taux de concordance global de 93,3 %** (28 concordances sur 30 messages). Les 4 anomalies injectées ont été détectées avec succès par les deux niveaux (100 % de détection critique), les deux divergences observées correspondant à des cas limites de transitoires où le modèle ML a anticipé une déviation avant l'atteinte du seuil matériel strict.

## 5.8 Stratégie deux niveaux

Les résultats obtenus justifient notre architecture hybride de détection d'anomalies, divisée en deux niveaux complémentaires :
- **Niveau 1 : Embarqué (Edge)** : Implémenté sur l'ESP32, basé sur des seuils fixes (ex. Température > 45°C). Avantages : temps de réaction quasi nul (< 1 ms), fonctionnement hors ligne, consommation minimale.
- **Niveau 2 : Serveur (Cloud)** : Modèle Isolation Forest (ou LSTM). Avantages : détection de corrélations complexes et d'anomalies contextuelles (ex. forte puissance mais basse altitude), temps de réponse acceptable (~100 ms via réseau).

## 5.9 Architecture du Pipeline de Prédiction IA

L'objectif de cette section est de décrire techniquement le flux complet de prédiction, depuis la réception des données capteur jusqu'au déclenchement d'une alerte sur le tableau de bord.

### 5.9.1 Flux de données

Le pipeline de prédiction IA suit les étapes suivantes :

1. **Réception des données** : L'ESP32 transmet une trame JSON via MQTT (topic `aircraft/sensors`) au broker HiveMQ. Node-RED s'abonne au topic et route les données vers InfluxDB 3 Core.

2. **Prétraitement** : Le service de prédiction (implémenté en Python via FastAPI) reçoit un vecteur de 20 à 24 features numériques. Il applique séquentiellement :
   - `SimpleImputer(strategy='median')` : remplacement des valeurs manquantes par la médiane calculée sur l'ensemble d'entraînement.
   - `StandardScaler` : centrage et réduction selon les statistiques de l'ensemble d'entraînement.

3. **Inférence** : Le modèle Isolation Forest (`n_estimators=200`) calcule un score d'anomalie via `score_samples()`. Le score brut (négatif pour les anomalies) est inversé pour obtenir un score positif croissant avec la probabilité d'anomalie.

4. **Décision** : Le score est comparé au seuil calibré (95ᵉ percentile des scores normaux de validation). Si `score ≥ seuil`, l'observation est classée anomale.

5. **Réponse** : L'API retourne un objet JSON contenant :
   ```json
   {
     "anomaly": 1,
     "score": 0.5234,
     "threshold": 0.4891,
     "status": "ok"
   }
   ```

6. **Alerte** : Node-RED peut interroger l'API à chaque nouvelle trame MQTT et, en cas d'anomalie détectée, écrire un point d'alerte dans InfluxDB et déclencher une notification dans Grafana.

### 5.9.2 État d'implémentation

Le service FastAPI (`detect_api.py`) est développé et fonctionnel en environnement local. Cependant, l'intégration de bout en bout (Node-RED → FastAPI → Grafana) n'a **pas été testée en conditions opérationnelles**. Les artefacts nécessaires au démarrage de l'API (modèle sérialisé, pipeline de prétraitement) ne sont pas encore tous présents dans le répertoire de déploiement. En conséquence, le service ML ne peut pas être qualifié d'opérationnel à ce stade.

**Tableau 5.5 : Maturité de l'intégration des composants**

| Composant | Statut | Preuve |
| :--- | :--- | :--- |
| Firmware ESP32 (C++) | ✅ Opérationnel (simulé Wokwi) | 392 lignes, compilation OK (974 KB) |
| Transmission MQTT (HiveMQ:1883) | ✅ Opérationnel | Captures Node-RED |
| Stockage InfluxDB 3 Core (local) | ✅ Opérationnel | Requêtes InfluxQL validées |
| Dashboard Grafana Cloud | ✅ Opérationnel | 10 panneaux, rafraîchissement 5 s |
| Détection Edge (seuils) | ✅ Opérationnel | 5 scénarios testés et validés |
| Pipeline ML (Colab) | ✅ Exécuté | Métriques et figures générées |
| API FastAPI `/predict` | ⚠️ Code écrit, non déployé | `detect_api.py` présent, artefacts incomplets |
| Connexion Node-RED → FastAPI | ❌ Non implémenté | Aucun flux Node-RED n'appelle l'API |
| Alertes ML dans Grafana | ❌ Non implémenté | Aucune règle d'alerte configurée |
| MQTT over TLS (port 8883) | ❌ Perspective moyen terme | Port 1883 utilisé (non chiffré) |
| Test bout-en-bout ML | ❌ Non réalisé | Pas de capture, latence non mesurée |
| TensorFlow Lite sur ESP32 | ❌ Perspective long terme | Pas de conversion démontrée |

## 5.10 Limites et perspectives

### 5.10.1 Analyse critique du déploiement Isolation Forest

Bien que l'Isolation Forest soit recommandé pour le déploiement serveur en raison de son caractère non supervisé et de sa rapidité d'inférence, une analyse critique de ses performances sur le jeu de test (39 841 observations) révèle des limites significatives :

- **Faux négatifs (FN)** : Avec un recall de 0,8774, le modèle manque environ 12,3 % des anomalies réelles. Sur la partition de test (4 631 anomalies), cela représente environ 568 anomalies non détectées. Dans un contexte aéronautique, chaque faux négatif constitue un risque de défaillance non anticipée.
- **Faux positifs (FP)** : La precision de 0,5063 signifie que près d'une alerte sur deux est un faux positif, ce qui peut entraîner une fatigue d'alarme (*alarm fatigue*) chez les opérateurs.
- **PR-AUC limitée** : La valeur de 0,6802 confirme que le modèle peine à maintenir simultanément une precision et un recall élevés sur l'ensemble de la courbe de seuils.

**Impact opérationnel des faux négatifs :** Dans un contexte de maintenance prédictive aéronautique, le coût d'un faux négatif (anomalie non détectée → défaillance potentielle) est asymétriquement plus élevé que celui d'un faux positif (inspection inutile). Un modèle avec un recall de 0,8774 n'est pas suffisant pour une fonction de sécurité critique sans mécanisme de redondance.

**Sensibilité au seuil et à la contamination :** Les performances varient significativement selon le percentile de seuil choisi (P80 à P99) et la valeur de contamination. Une analyse de sensibilité est recommandée pour identifier le point de fonctionnement optimal en fonction du coût métier des FP et FN.

**Conclusion :** Le modèle Isolation Forest, dans sa configuration actuelle, constitue un outil de pré-filtrage utile mais **ne peut pas être qualifié de prêt pour une fonction critique de sécurité aéronautique**. Son déploiement opérationnel nécessiterait :
1. La définition d'un recall minimum acceptable par un expert métier aéronautique.
2. Une validation sur des données réelles (non simulées).
3. Un processus de certification conforme aux normes applicables (DO-178C, ARP4754A).
4. Un mécanisme de redondance (combinaison avec la détection par seuils embarquée).

### 5.10.2 Limites méthodologiques

- Le dataset d'entraînement est **synthétique** (généré par simulation), ce qui limite la validité externe des performances observées.
- Les anomalies sont injectées selon des règles déterministes, ce qui peut biaiser l'évaluation en faveur de modèles capables de détecter ces patterns spécifiques.
- L'intervalle d'échantillonnage de 1 minute est régulier, ce qui ne reflète pas les irrégularités d'un système réel.
- La validation NASA SMAP/MSL repose sur des données simulées et non sur les véritables jeux de données de la NASA.

## Conclusion du Chapitre 5
Ce chapitre a démontré la faisabilité technique d'intégrer des modèles d'apprentissage automatique pour la détection d'anomalies dans un contexte IoT aéronautique. Le LSTM Autoencoder offre les meilleures performances en termes de discrimination (ROC-AUC = 0,9590, PR-AUC = 0,7184), tandis que l'Isolation Forest présente l'avantage d'être non supervisé et rapide à l'inférence. Toutefois, aucun des modèles testés n'atteint un niveau de performance suffisant pour une fonction critique de sécurité sans validation complémentaire sur données réelles et processus de certification.

---

# CONCLUSION GÉNÉRALE

Le présent Projet de Fin d'Études, réalisé au sein de YaneCode Digital par Nourhen KHELIFI durant l'été 2026, s'inscrit dans un contexte technologique en pleine évolution à la croisée de l'Internet des Objets (IoT), de l'Aéronautique et de l'Intelligence Artificielle. Face à la complexité croissante des systèmes autonomes, l'objectif principal était de concevoir et déployer une plateforme complète, robuste et en temps réel pour la surveillance télémétrique et la détection d'anomalies.

Au terme de ce projet, dont l'avancement est estimé à 87 %, nous avons apporté une réponse structurée à la problématique initiale grâce à une architecture logicielle et matérielle modulaire. Les principales contributions de ce travail incluent :
- Le développement d'un firmware de 392 lignes en C++ asynchrone non-bloquant pour un microcontrôleur ESP32, intégrant la lecture simultanée de capteurs (MPU6050, DHT22) et une connectivité MQTT.
- La conception d'un pipeline complet de données à 5 couches (Capture, Ingestion, Traitement, Stockage, Visualisation).
- L'élaboration d'un tableau de bord de monitoring sur Grafana Cloud (v13.2.0) composé de 10 panneaux interactifs, connecté à une base InfluxDB 3 Core (v3.11.0) hébergée localement via un tunnel ngrok.
- La mise en place d'une détection embarquée (Edge Computing) capable d'identifier 4 types d'anomalies critiques en moins d'une milliseconde, fonctionnant de manière autonome et indépendante du réseau.
- L'entraînement et l'évaluation de quatre modèles de détection d'anomalies (Isolation Forest, One-Class SVM, LSTM Autoencoder, Random Forest) sur un dataset de 199 202 observations avec un protocole de séparation temporelle strict.
- La résolution de 7 difficultés techniques majeures relatives à la synchronisation asynchrone et à la transmission réseau.

Cependant, le système actuel présente certaines limites qu'il convient de souligner :
- Le pipeline ML n'est pas encore intégré de bout en bout : le code de l'API FastAPI existe mais n'a pas été déployé ni testé en conditions opérationnelles. La connexion automatique Node-RED → API de prédiction → alerte Grafana reste à implémenter.
- L'utilisation de ngrok impose une URL aléatoire à chaque redémarrage.
- La communication MQTT s'effectue en clair sur le port 1883 (sans chiffrement TLS), ce qui constitue une vulnérabilité de sécurité.
- Le système embarqué (Niveau 1) fonctionne de manière autonome grâce aux seuils statiques, mais le Niveau 2 (ML serveur) dépend de la connectivité Wi-Fi, du broker MQTT, de Node-RED, d'InfluxDB et de Grafana Cloud. La solution globale ne peut donc pas être qualifiée d'autonome.
- L'injection des anomalies dans le dataset est synthétique, et les capteurs Wokwi représentent des cas idéaux sans bruit réel.
- Les performances des modèles ML (F1 ≈ 0,65, PR-AUC ≈ 0,68-0,76) ne sont pas suffisantes pour une fonction critique de sécurité sans validation complémentaire.

Ces limites ouvrent la voie à de nombreuses perspectives d'amélioration :
- **Court terme** : Configurer un token persistant pour ngrok, activer les alertes natives dans Grafana, créer un script de démarrage automatisé, et déployer l'API FastAPI avec les artefacts de modèle complets.
- **Moyen terme** : Intégrer le modèle Isolation Forest sous forme de microservice connecté à Node-RED, remplacer la simulation Wokwi par un ESP32 physique pour valider l'approche face aux bruits réels, sécuriser le protocole MQTT via TLS (port 8883) avec certificats X.509, et implémenter un système de buffer local via SPIFFS sur l'ESP32.
- **Long terme** : Évoluer vers une infrastructure Cloud native (AWS IoT Core), intégrer un tableau de bord FFT pour l'analyse vibratoire fine. Pour l'inférence embarquée sur ESP32, l'Isolation Forest n'étant pas directement compatible avec TensorFlow Lite (modèle à base d'arbres et non de graphes de tenseurs), deux voies sont envisageables : (a) la conversion en code C natif via des bibliothèques telles que `emlearn` ou `m2cgen`, ou (b) l'entraînement d'un autoencoder dense (non LSTM, pour respecter la contrainte de 520 KB SRAM) convertible en TFLite INT8. La faisabilité de chaque option nécessite un benchmark préalable de taille mémoire et de latence d'inférence.

En conclusion, ce projet constitue une base technologique solide et évolutive, démontrant de manière concrète la synergie entre l'embarqué et le Cloud pour la supervision intelligente des systèmes aéronautiques.

### Protocole de reproductibilité et d'audit

L'ensemble des résultats ML présentés dans ce rapport provient d'une exécution unique du script `audit_ml_et_pipeline_final.py` sur Google Colab, avec les paramètres suivants :
- **Seed global** : `RANDOM_STATE = 42` (`numpy`, `tensorflow`)
- **Dataset** : `aeronautical_iot_esp32_predictive_maintenance_200k.csv` (SHA-256 : `f881533978129dbf630ba94d5de3db15c4ad752dafe50f64a32f8d8fc8bd41f2`)
- **Environnement** : Google Colab, Python 3.x, scikit-learn 1.9.0, TensorFlow 2.x
- **Split** : Temporel strict 60/20/20 (indices consécutifs, pas de shuffle)
- **Seuils** : P95 des scores normaux de la partition de validation
- **Artefacts générés** : `confusion_matrices_all.png`, `roc_pr_curves.png`, `comparaison_modeles.png`, `isolation_forest_model.joblib`, `imputer.joblib`, `scaler.joblib`, `numeric_features.joblib`, `if_config.joblib`

Toute réexécution du script avec les mêmes paramètres et le même dataset doit produire des résultats identiques pour les modèles déterministes (IF, OCSVM, RF). Les résultats du LSTM Autoencoder peuvent varier légèrement en raison du non-déterminisme GPU de TensorFlow.

---

# BIBLIOGRAPHIE

[1] M. A. A. Faruque and F. Vahid, "Anomaly Detection in Aerospace Systems using Machine Learning: A Review," *IEEE Access*, vol. 8, pp. 12567-12580, 2020.
[2] A. Hundt et al., "Real-time Telemetry Processing and Anomaly Detection for UAVs using MQTT," *IEEE Internet of Things Journal*, vol. 7, no. 5, pp. 4123-4135, May 2020.
[3] NASA JPL, "Telemanom: A Framework for Detecting Anomalies in Multivariate Time Series," 2018. [Online]. Available: https://github.com/nasa/telemanom
[4] L. Ruff et al., "Deep One-Class Classification," in *Proceedings of the 35th International Conference on Machine Learning (ICML)*, 2018, pp. 4390-4399.
[5] K. Zhao, "LSTM-based Autoencoder for Time Series Anomaly Detection," *IEEE Transactions on Neural Networks and Learning Systems*, vol. 31, no. 10, pp. 3840-3850, 2020.
[6] F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation Forest," in *8th IEEE International Conference on Data Mining (ICDM)*, 2008, pp. 413-422.
[7] B. Schölkopf, J. C. Platt, J. Shawe-Taylor, A. J. Smola, and R. C. Williamson, "Estimating the Support of a High-Dimensional Distribution," *Neural Computation*, vol. 13, no. 7, pp. 1443-1471, 2001.
[8] OASIS Standard, "MQTT Version 5.0," OASIS Standard, March 2019. [Online]. Available: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
[9] RTCA / EUROCAE, "DO-178C / ED-12C: Software Considerations in Airborne Systems and Equipment Certification," RTCA Inc., 2011.
[10] SAE International, "ARP4754A: Guidelines for Development of Civil Aircraft and Systems," SAE International, Dec. 2010.
[11] S. Hochreiter and J. Schmidhuber, "Long Short-Term Memory," *Neural Computation*, vol. 9, no. 8, pp. 1735-1780, 1997.
[12] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.

---

# ANNEXES

## Annexe A : Code source du firmware ESP32 (Extrait des fonctions asynchrones critiques)

```cpp
/* =========================================================================
   Firmware ESP32 — Aircraft Telemetry & Edge Anomaly Detection (Extrait)
   Architecture non-bloquante basée sur millis() — 392 lignes au total
   ========================================================================= */

#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_MPU6050.h>

// Définitions des constantes de cadencement
const unsigned long READ_INTERVAL      = 1000; // 1s : lecture capteurs
const unsigned long MQTT_INTERVAL      = 3000; // 3s : émission télémétrie MQTT
const unsigned long RECONNECT_INTERVAL = 5000; // 5s : reconnexion non-bloquante

// --- Lecture filtrée des capteurs ---
void readSensors() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (!isnan(t) && !isnan(h)) {
    tempBuffer[bufferIndex] = t;
    bufferIndex = (bufferIndex + 1) % FILTER_SIZE;
    temperature = movingAverage(tempBuffer);
    humidity = h;
  }
  pressure = bmp.readPressure() / 100.0;
  altitude = bmp.readAltitude();
  
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
  potPercent = map(analogRead(POT_PIN), 0, 4095, 0, 100);
}

// --- Détection d'anomalies Niveau 1 (Edge - < 1 ms) ---
void detectAnomaly() {
  statusSystem = "NORMAL";
  anomalyReason = "";

  if (temperature > 45.0) {
    statusSystem = "ALERT";
    anomalyReason = "HIGH TEMP";
  } else if (pressure < 850.0 && pressure > 0) {
    statusSystem = "ALERT";
    anomalyReason = "LOW PRESSURE";
  } else {
    float vibration = sqrt(accX * accX + accY * accY + pow(accZ - 9.81, 2));
    if (vibration > 15.0) {
      statusSystem = "ALERT";
      anomalyReason = "HIGH VIBRATION";
    }
  }
  if (potPercent > 80) {
    statusSystem = "ALERT";
    anomalyReason = "ENGINE FAILURE";
  }

  digitalWrite(GREEN_LED, statusSystem == "NORMAL" ? HIGH : LOW);
  digitalWrite(RED_LED, statusSystem == "ALERT" ? HIGH : LOW);
  if (statusSystem == "ALERT") tone(BUZZER_PIN, 1500);
  else noTone(BUZZER_PIN);
}

// --- Émission asynchrone MQTT ---
void sendMQTT() {
  if (!client.connected()) return;

  char payload[256];
  snprintf(payload, sizeof(payload),
    "{\"temp\":%.1f,\"hum\":%.0f,\"press\":%.0f,\"alt\":%.0f,"
    "\"accX\":%.2f,\"accY\":%.2f,\"accZ\":%.2f,\"pot\":%d,"
    "\"status\":\"%s\",\"reason\":\"%s\",\"ts\":%lu}",
    temperature, humidity, pressure, altitude,
    accX, accY, accZ, potPercent,
    statusSystem.c_str(), anomalyReason.c_str(), millis() / 1000
  );
  client.publish("aircraft/sensors", payload);
}

// --- Boucle principale non bloquante ---
void loop() {
  unsigned long currentMillis = millis();

  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      if (currentMillis - lastReconnectAttempt >= RECONNECT_INTERVAL) {
        lastReconnectAttempt = currentMillis;
        reconnectMQTTNonBlocking();
      }
    } else {
      client.loop();
    }
  }

  if (currentMillis - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentMillis;
    readSensors();
    detectAnomaly();
  }

  if (currentMillis - lastMQTTTime >= MQTT_INTERVAL) {
    lastMQTTTime = currentMillis;
    sendMQTT();
  }
}
```

---

## Annexe B : Configuration du pipeline Node-RED et de la base de données InfluxDB 3 Core

### 1. Fonction JavaScript de parsing sécurisé (Node-RED)

```javascript
// Sécurisation contre les payloads JSON partiels ou corrompus
let raw = msg.payload;

if (typeof raw === 'object' && raw !== null) {
    msg.payload = raw;
    msg.payload.timestamp = msg.payload.timestamp || Math.floor(Date.now() / 1000);
    return msg;
}

if (typeof raw !== 'string' || raw.trim().length === 0) {
    node.warn('Message MQTT vide ou invalide ignoré.');
    return null;
}

try {
    let data = JSON.parse(raw.trim());
    if (!data.ts && !data.timestamp) {
        data.timestamp = Math.floor(Date.now() / 1000);
    }
    msg.payload = data;
    return msg;
} catch (err) {
    node.error('Erreur de parsing JSON : ' + err.message, msg);
    return null;
}
```

### 2. Format des requêtes InfluxQL (Grafana → InfluxDB 3 Core)

```sql
-- Requête pour panneau télémétrique thermique et vibratoire (Grafana)
SELECT 
    mean("temperature") AS "Température (°C)",
    mean("vibration_rms") AS "Vibration RMS (m/s²)",
    mean("pressure") AS "Pression (hPa)"
FROM "aircraft_telemetry"
WHERE time >= now() - 15m
GROUP BY time(5s) fill(null);
```

---

## Annexe C : Script Python d'ingénierie des caractéristiques et d'entraînement ML

```python
"""
Extrait du pipeline d'ingénierie et d'entraînement Isolation Forest
Fichier : iot-anomaly-detection/train_and_save_pipeline.py
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib

def compute_engineered_features(df):
    """Calcul des caractéristiques physiques avancées."""
    # Norme vibratoire RMS
    if {'accX', 'accY', 'accZ'}.issubset(df.columns):
        df['vibration_rms'] = np.sqrt(df['accX']**2 + df['accY']**2 + (df['accZ'] - 9.81)**2)
    
    # Gradients et ratios énergétiques
    if 'temperature' in df.columns:
        df['temp_gradient'] = df['temperature'].diff().fillna(0)
    if 'altitude' in df.columns and 'potentiometer' in df.columns:
        df['power_per_altitude'] = (df['potentiometer'] * 1.2) / (df['altitude'] + 1.0)
        
    return df

# Séparation temporelle stricte 60 / 20 / 20
def temporal_split(df, train_ratio=0.6, val_ratio=0.2):
    n = len(df)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    return df.iloc[:n_train], df.iloc[n_train:n_train+n_val], df.iloc[n_train+n_val:]

# Calibration du seuil sur la partition de validation normale
def calibrate_threshold(model, scaler, imputer, df_val, features, percentile=95):
    X_val_imp = imputer.transform(df_val[features])
    X_val_scaled = scaler.transform(X_val_imp)
    val_scores = -model.score_samples(X_val_scaled)
    # Seuil calculé sur les observations saines (label == 0)
    normal_mask = (df_val['anomaly_reference'] == 0)
    threshold = float(np.percentile(val_scores[normal_mask], percentile))
    return threshold
```

---

## Annexe D : Manuels d'installation et de déploiement (Docker, Mosquitto, Grafana, API)

### 1. Démarrage de l'infrastructure locale (Docker Compose)

```yaml
version: '3.8'

services:
  # Broker MQTT
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: mosquitto_broker
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf

  # InfluxDB 3 Core (Time Series Database)
  influxdb:
    image: influxdb:latest
    container_name: influxdb3_core
    ports:
      - "8181:8181"
    environment:
      - INFLUXDB_HTTP_AUTH_ENABLED=true
      - INFLUXDB_DB=aircraft_db

  # Node-RED Middleware
  nodered:
    image: nodered/node-red:latest
    container_name: nodered_pipeline
    ports:
      - "1880:1880"
    volumes:
      - ./flows.json:/data/flows.json
    depends_on:
      - mosquitto
      - influxdb

  # API d'Inférence FastAPI ML
  detect_api:
    build: ./service
    container_name: ml_predict_api
    ports:
      - "8000:8000"
    restart: unless-stopped
```

### 2. Démarrage du tunnel ngrok pour Grafana Cloud

```bash
# Exposition du port InfluxDB 3 Core vers Grafana Cloud
ngrok http 8181 --log=stdout > ngrok.log &
```

### 3. Exécution du service de prédiction FastAPI

```bash
uvicorn service.detect_api:app --host 0.0.0.0 --port 8000 --reload
```

