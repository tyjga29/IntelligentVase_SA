#include <M5Stack.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <WiFiNINA.h>

const int inputPin = 2;
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";
const char* mqttServer = "MQTT_BROKER_IP";
const int mqttPort = "MQTT_PORT";
const char mqttTopic = "LIGHTSENSOR_TOPIC"
const char* mqttUser = "MQTT_USERNAME";
const char* mqttPassword = "MQTT_PASSWORD";

WiFiSSLClient wifiClient;
PubSubClient client(espClient);
int lightValue = 0;

//SetUp M5 Lightsensor, Wifi-Connection and MQTT-Connection
 void setup() {
  Serial.behin(9600);
  M5.begin();
  pinMode(inputPin, INPUT);

  connectWifi();

  client.setServer(mqttServer, mqttPort);
  client.setCallBack(callback);
  client.subscribe(mqttTopic);
}

// Gets the value from the Input and compares it to the one before. If it is different, the value is sent
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int previousLightValue = lightValue;
  int sensorReading = digitalRead(inputPin);

  if (sensorReading != previousLightValue) {
    lightValue = sensorReading;
    char message[50];
    sprintf(message, "%d", lightValue);
    client.publish("sensor/light", message);
  }

  delay(1000); 
}

void connectWiFi() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    if (WiFi.begin(ssid, password) != WL_CONNECTED) {
      Serial.println("Connection Failed! Rebooting...");
      delay(5000);
      ESP.restart();
    }
  }
  Serial.println("Connected to WiFi");
}

// Logic to implement a base resistance. The light should only measure sunlight, meaning the resistance should be on the level of the base-brightness of the room
void callback(char* topic, byte* payload, unsigned int length) {
  String receivedPayload;
  for (int i = 0; i < length; i++) {
    receivedPayload += (char)payload[i];
  }
  // Have to wait until we know how the sensor works
  int newResistance = receivedPayload.toInt();
}

void reconnect() {
  while (!client.connected()) {
    M5.Lcd.print("Connecting to MQTT...");
    if (client.connect("ArduinoClient", mqttUser, mqttPassword)) {
    } else {
      delay(5000);
    }
  }
}
