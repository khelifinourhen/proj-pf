# 🛰️ Module IoT Embarqué (Edge ESP32)

Ce module contient le code source du microcontrôleur **ESP32** et la configuration de simulation **Wokwi** pour la collecte et la transmission des mesures capteurs aéronautiques.

## 📁 Contenu
- sketch.ino : Code source Arduino C++ de l'ESP32 (génération de télémétrie, capteurs température, pression, vibrations, envoi HTTP / MQTT).
- diagram.json : Schéma de câblage électronique Wokwi.
- libraries.txt : Bibliothèques Arduino requises (WiFi, ArduinoJson, PubSubClient).
- wokwi.toml : Fichier de configuration du simulateur Wokwi.
- ircraft-esp32.code-workspace : Espace de travail VS Code préconfiguré.

## 🚀 Lancement de la Simulation
1. **Dans VS Code** :
   - Installez l'extension **Wokwi for VS Code**.
   - Ouvrez diagram.json et démarrez la simulation.
2. **Sur Wokwi Web (Cloud)** :
   - Rendez-vous sur [Wokwi.com](https://wokwi.com/).
   - Importez sketch.ino et diagram.json.
