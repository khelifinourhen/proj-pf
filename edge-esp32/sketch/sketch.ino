
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <time.h>

// ================= WIFI / MQTT =================
const char* ssid = "Wokwi-GUEST";
const char* password = "wokwi";

const char* mqtt_server = "broker.hivemq.com";
const int   mqtt_port   = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
char mqttClientId[32];

// ================= PIN CONFIG =================
#define DHTPIN 15
#define DHTTYPE DHT22
#define POT_PIN 34
#define BUTTON_PIN 13
#define GREEN_LED 26
#define RED_LED 27
#define BUZZER_PIN 25

// ================= OBJECTS =================
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;
Adafruit_MPU6050 mpu;
LiquidCrystal_I2C lcd(0x27, 20, 4);

// ================= VARIABLES =================
float temperature = 0, humidity = 0, pressure = 0, altitude = 0;
float accX = 0, accY = 0, accZ = 0;
int potPercent = 0;
int selectedSensor = 0; // sert uniquement à choisir la page LCD
String statusSystem = "NORMAL";
String anomalyReason = "";

// ================= TIMERS (tout en millis(), non bloquant) =====
unsigned long lastReadTime = 0;
unsigned long lastSerialTime = 0;
unsigned long lastLCDTime = 0;
unsigned long lastMQTTTime = 0;
unsigned long lastButtonCheck = 0;
unsigned long lastReconnectAttempt = 0;

const unsigned long READ_INTERVAL       = 1000;  // 1s : lecture capteurs
const unsigned long SERIAL_INTERVAL     = 2000;  // 2s : debug serial
const unsigned long LCD_INTERVAL        = 1000;  // 1s : rafraîchissement LCD
const unsigned long MQTT_INTERVAL       = 3000;  // 3s : envoi MQTT
const unsigned long BUTTON_DEBOUNCE_MS  = 200;   // anti-rebond non bloquant
const unsigned long RECONNECT_INTERVAL  = 5000;  // tentative reconnexion MQTT

// ================= FILTER =================
#define FILTER_SIZE 5
float tempBuffer[FILTER_SIZE];
int bufferIndex = 0;

float movingAverage(float buffer[]) {
  float sum = 0;
  for (int i = 0; i < FILTER_SIZE; i++) sum += buffer[i];
  return sum / FILTER_SIZE;
}

// ================= WIFI =================
void setup_wifi() {
  Serial.println("WiFi connecting...");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500); // acceptable ici : une seule fois, dans setup()
    Serial.print(".");
    attempts++;
  }
  Serial.println();
  Serial.println(WiFi.status() == WL_CONNECTED ? "WiFi OK" : "WiFi FAIL");
}

// ================= NTP (pour le vrai timestamp) =================
void setup_time() {
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("Synchronisation NTP");
  time_t now = time(nullptr);
  int tries = 0;
  while (now < 1700000000 && tries < 15) { // attend un temps "plausible"
    delay(300);
    Serial.print(".");
    now = time(nullptr);
    tries++;
  }
  Serial.println();
  if (now >= 1700000000) {
    Serial.println("✓ Heure NTP synchronisée");
  } else {
    Serial.println("✗ NTP indisponible, on utilisera millis() en secours");
  }
}

// Renvoie un timestamp epoch (secondes). Si NTP a échoué,
// renvoie un timestamp "relatif" basé sur millis() (moins bon
// mais évite d'envoyer un champ vide/faux).
unsigned long getTimestamp() {
  time_t now = time(nullptr);
  if (now > 1700000000) return (unsigned long)now;
  return millis() / 1000UL;
}

// ================= MQTT =================
void reconnectMQTT_nonBlocking() {
  if (client.connected()) return;
  unsigned long now = millis();
  if (now - lastReconnectAttempt < RECONNECT_INTERVAL) return; // pas de blocage
  lastReconnectAttempt = now;

  Serial.print("MQTT connecting as ");
  Serial.print(mqttClientId);
  Serial.print(" ... ");
  if (client.connect(mqttClientId)) {
    Serial.println("OK");
    client.subscribe("aircraft/cmd"); // optionnel : commandes entrantes
  } else {
    Serial.print("fail, state=");
    Serial.println(client.state());
  }
}

// ================= BUTTON (non bloquant) =================
void checkButton() {
  static bool lastButtonState = HIGH;
  unsigned long now = millis();
  if (now - lastButtonCheck < 20) return; // léger anti-bruit, sans delay()
  lastButtonCheck = now;

  bool currentState = digitalRead(BUTTON_PIN);
  static unsigned long lastPress = 0;
  if (lastButtonState == HIGH && currentState == LOW && (now - lastPress) > BUTTON_DEBOUNCE_MS) {
    selectedSensor = (selectedSensor + 1) % 3; // change juste la page LCD
    lastPress = now;
    Serial.print("Page LCD -> capteur ");
    Serial.println(selectedSensor);
  }
  lastButtonState = currentState;
}

// ================= READ SENSORS =================
void readSensors() {
  // DHT22
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (!isnan(t) && !isnan(h)) {
    tempBuffer[bufferIndex] = t;
    bufferIndex = (bufferIndex + 1) % FILTER_SIZE;
    temperature = movingAverage(tempBuffer);
    humidity = h;
  }

  // BMP180
  pressure = bmp.readPressure() / 100.0;
  altitude = bmp.readAltitude();

  // MPU6050
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;

  // Potentiomètre
  potPercent = map(analogRead(POT_PIN), 0, 4095, 0, 100);

  // --- Simulation de défaut : TOUS les capteurs réagissent au pot ---
  // Avant : seul le capteur "selectedSensor" changeait (switch/case).
  // Maintenant : au-delà de 50%, les trois groupes varient ensemble,
  // proportionnellement à la position du potentiomètre. Cela permet
  // de tester tous les capteurs en même temps, sans devoir appuyer
  // sur le bouton.
  if (potPercent > 50) {
    float factor = (potPercent - 50) / 50.0; // 0.0 -> 1.0
    temperature += 25.0 * factor;
    pressure    -= 250.0 * factor;
    altitude    += 1500.0 * factor;
    accX        += 20.0 * factor;
    accY        += 20.0 * factor;
    accZ        += 20.0 * factor;
  }
}

// ================= ANOMALY DETECTION =================
void detectAnomaly() {
  statusSystem = "NORMAL";
  anomalyReason = "";

  if (temperature > 45) {
    statusSystem = "ALERT";
    anomalyReason = "HIGH TEMP";
  } else if (pressure < 850 && pressure > 0) {
    statusSystem = "ALERT";
    anomalyReason = "LOW PRESSURE";
  } else {
    float vibration = sqrt(accX*accX + accY*accY + pow(accZ-9.8, 2));
    if (vibration > 15) {
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
  if (statusSystem == "ALERT") {
    tone(BUZZER_PIN, 1500);
  } else {
    noTone(BUZZER_PIN);
  }
}

// ================= LCD =================
void displayLCD() {
  static String lastDisplay = "";
  String currentDisplay = String(temperature,1) + "|" + String(humidity,0) + "|" +
                          String(pressure,0) + "|" + statusSystem;

  if (currentDisplay != lastDisplay) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Aircraft Monitor");
    lcd.setCursor(0, 1);
    lcd.print("T:");
    lcd.print(temperature, 1);
    lcd.print("C H:");
    lcd.print(humidity, 0);
    lcd.setCursor(0, 2);
    lcd.print("P:");
    lcd.print(pressure, 0);
    lcd.print(" A:");
    lcd.print(altitude, 0);
    lcd.setCursor(0, 3);
    if (statusSystem == "NORMAL")
      lcd.print("STATUS NORMAL");
    else
      lcd.print(anomalyReason);

    lastDisplay = currentDisplay;
  }
}

// ================= MQTT SEND =================
void sendMQTT() {
  if (!client.connected()) return; // pas de tentative bloquante ici

  String payload = "{";
  payload += "\"timestamp\":" + String(getTimestamp()) + ",";
  payload += "\"temperature\":" + String(temperature, 2) + ",";
  payload += "\"humidity\":" + String(humidity, 2) + ",";
  payload += "\"pressure\":" + String(pressure, 2) + ",";
  payload += "\"altitude\":" + String(altitude, 2) + ",";
  payload += "\"accX\":" + String(accX, 2) + ",";
  payload += "\"accY\":" + String(accY, 2) + ",";
  payload += "\"accZ\":" + String(accZ, 2) + ",";
  payload += "\"potentiometer\":" + String(potPercent) + ",";
  payload += "\"status\":\"" + String(statusSystem) + "\",";
  payload += "\"reason\":\"" + String(anomalyReason) + "\"";
  payload += "}";
Serial.println("========== MQTT JSON ==========");
Serial.println(payload);
Serial.println("===============================");
  bool ok = client.publish("aircraft/sensors", payload.c_str());
  Serial.print("MQTT publish ");
  Serial.println(ok ? "OK" : "FAILED");
}

// ================= SERIAL DEBUG (allégé) =================
void printDebugInfo() {
  Serial.print("T:"); Serial.print(temperature, 1);
  Serial.print(" H:"); Serial.print(humidity, 0);
  Serial.print(" P:"); Serial.print(pressure, 0);
  Serial.print(" A:"); Serial.print(altitude, 0);
  Serial.print(" Pot:"); Serial.print(potPercent); Serial.print("%");
  Serial.print(" WiFi:"); Serial.print(WiFi.status() == WL_CONNECTED ? "OK" : "KO");
  Serial.print(" MQTT:"); Serial.print(client.connected() ? "OK" : "KO");
  Serial.print(" Heap:"); Serial.print(ESP.getFreeHeap());
  Serial.print(" |"); Serial.print(statusSystem);
  if (statusSystem == "ALERT") {
    Serial.print(":"); Serial.print(anomalyReason);
  }
  Serial.println();
}

// ================= SETUP =================
void setup() {
 Serial.begin(115200);
  delay(1000); // court, une seule fois, pour laisser le moniteur s'ouvrir

  Serial.println("\n=== Aircraft Monitor - demarrage ===");

  Wire.begin(21, 22);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);

  for (int i = 0; i < FILTER_SIZE; i++) tempBuffer[i] = 0;

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Init...");

  dht.begin();

  if (!bmp.begin())  Serial.println("✗ BMP180 ERROR");
  else               Serial.println("✓ BMP180 OK");

  if (!mpu.begin())  Serial.println("✗ MPU6050 ERROR");
  else               Serial.println("✓ MPU6050 OK");

  setup_wifi();
  if (WiFi.status() == WL_CONNECTED) setup_time();

  // Identifiant MQTT unique basé sur l'adresse MAC (évite les
  // déconnexions dues à un clientId dupliqué sur un broker public)
  snprintf(mqttClientId, sizeof(mqttClientId), "AircraftESP32-%s",
           WiFi.macAddress().c_str());

  client.setServer(mqtt_server, mqtt_port);
  client.setBufferSize(512); // marge de sécurité pour le payload JSON
  reconnectMQTT_nonBlocking();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("SYSTEM READY");

  Serial.println("=== SYSTEM READY ===");
  

  
}



// ================= LOOP (100% non bloquant) =================
void loop() {
  unsigned long currentMillis = millis();
  // SUPPRIMÉ : while (!Serial) { delay(10); }
  // → Sur ESP32/Wokwi, cette boucle bloquait toute la simulation
  //   car Serial n'est pas un objet USB-CDC comme sur Arduino Leonardo.

  checkButton();

  if (currentMillis - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentMillis;
    readSensors();
    detectAnomaly();
  }

  if (currentMillis - lastLCDTime >= LCD_INTERVAL) {
    lastLCDTime = currentMillis;
    displayLCD();
  }

  if (currentMillis - lastSerialTime >= SERIAL_INTERVAL) {
    lastSerialTime = currentMillis;
    printDebugInfo();
  }

  reconnectMQTT_nonBlocking();
  if (client.connected()) {
    client.loop();
  }

  if (currentMillis - lastMQTTTime >= MQTT_INTERVAL) {
    lastMQTTTime = currentMillis;
    sendMQTT();
  }

  // Pas de delay() ici : c'est la principale cause de "latence"
  // perçue dans Wokwi (chaque delay() bloque toute la simulation).
}