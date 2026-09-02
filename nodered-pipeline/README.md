# 🔄 Pipeline d'Orchestration Node-RED

Ce module gère le flux de données IoT, la réception MQTT/HTTP, l'aiguillage vers l'API d'inférence ML, et l'insertion dans InfluxDB.

## 📁 Contenu
- lows.json / low.json : Définition complète des nœuds et du pipeline de données Node-RED.
- Dockerfile : Conteneur prêt pour hébergement cloud (Render / Railway).

## 🚀 Utilisation
- **Localement** : Lancez 
ode-red dans votre terminal, ouvrez http://localhost:1880, puis cliquez sur le menu en haut à droite > **Import** > sélectionnez lows.json.
