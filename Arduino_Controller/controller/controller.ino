#include <ArduinoMqttClient.h>
#include <WiFiS3.h>

#include "arduino_secrets/arduino_secrets.h"

//WiFi Variables
const char ssid[] = SECRET_SSID;   
const char pass[] = SECRET_PASS;   

const char* mqtt_broker = MQTT_BROKER;
const int mqtt_port = MQTT_PORT;

const char* light_topic = LIGHT_DATA_TOPIC;
const char* moisture_topic = MOISTURE_DATA_TOPIC;

const long interval = INTERVAL_SEND;

const int LightDigital_Input = LIGHT_DIGITAL_INPUT;
const int LightAnalog_Input = LIGHT_ANALOG_INPUT;
const int WaterpumpDigital_Output = WATERPUMP_DIGITAL_OUTPUT;
const int MoistureAnalog_Input = MOISTURE_ANALOG_INPUT;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);

  setupWifiAndMQTT();
  setupSensors();
}

void loop() {
  int light_value = analogRead(LightAnalog_Input);
  int moisture_value = analogRead(MoistureAnalog_Input);

  Serial.print("Light Value: ");
  Serial.println(light_value);
  sendDataOverMQTT(light_value, light_topic);

  Serial.print("Moisture Value: ");
  Serial.println(moisture_value);
  sendDataOverMQTT(moisture_value, moisture_topic);

  delay(5000);
}

void setupSensors() {
  pinMode(LightDigital_Input, INPUT);
  pinMode(LightAnalog_Input, INPUT);
  pinMode(WaterpumpDigital_Output, OUTPUT);
  pinMode(MoistureAnalog_Input, INPUT);
}

void setupWifiAndMQTT() {
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print("Connection to WPA SSID ");
    Serial.print(ssid);
    Serial.println(" failed. Retrying...");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(mqtt_broker);

  if (!mqttClient.connect(mqtt_broker, mqtt_port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void sendDataOverMQTT(int data, const char* topic) {
  Serial.print("Sending message to topic: ");
  Serial.println(topic);

  //send message, the Print interface can be used to set the message contents
  mqttClient.beginMessage(topic);
  mqttClient.print(data);
  mqttClient.endMessage();
}
