# Script pour envoyer des donnees de test directement a InfluxDB Cloud
import time
import urllib.request
import urllib.error

INFLUX_URL = "https://eu-central-1-1.aws.cloud2.influxdata.com"
ORG = "16de2b41623de972"
BUCKET = "aircraft_telemetry"

TOKEN = input("Entrez votre Token InfluxDB Cloud : ").strip()

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "text/plain; charset=utf-8",
    "Accept": "application/json"
}

write_url = f"{INFLUX_URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=s"

print(f"\nEnvoi de donnees de test vers {write_url}...")

points = []
now = int(time.time())

# 10 points normaux (derniers 100 secondes)
for i in range(10):
    t = now - (10 - i) * 10
    temp = 24.0 + (i * 0.5)
    pres = 1013.0 - (i * 1.0)
    vib = 0.12 + (i * 0.02)
    rpm = 1450.0 + (i * 10)
    line = f'sensors_ml,device=ESP32 temperature_c={temp},pressure_hpa={pres},vibration_norm_ms2={vib},rpm={rpm},ml_anomaly=0,ml_anomaly_score=0.18,ml_status="NORMAL" {t}'
    points.append(line)

# 5 points anomalie (tres recents)
for i in range(5):
    t = now - 5 + i
    temp = 95.0 + (i * 8.0)
    pres = 650.0 - (i * 10.0)
    vib = 8.5 + (i * 2.0)
    rpm = 4800.0 + (i * 200)
    line = f'sensors_ml,device=ESP32 temperature_c={temp},pressure_hpa={pres},vibration_norm_ms2={vib},rpm={rpm},ml_anomaly=1,ml_anomaly_score=0.89,ml_status="ANOMALY" {t}'
    points.append(line)

payload = "\n".join(points).encode("utf-8")

try:
    req = urllib.request.Request(write_url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        if response.status in (200, 204):
            print("\n[SUCCES] 15 points de telemetrie envoyes avec succes a InfluxDB Cloud !")
            print("Rechargez votre dashboard Grafana : les graphiques vont apparaitre !")
except urllib.error.HTTPError as e:
    print(f"\n[ERREUR HTTP {e.code}] : {e.read().decode()}")
except Exception as e:
    print(f"\n[ERREUR] : {e}")
