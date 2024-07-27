#include <ArduinoMqttClient.h>
#include <WiFiS3.h>
#include "DHT.h"

#include "arduino_secrets/arduino_secrets.h"

//WiFi Variables
const char ssid[] = SECRET_SSID;   
const char pass[] = SECRET_PASS;   

//MQTT Variables
const char* mqtt_broker = MQTT_BROKER;
const int mqtt_port = MQTT_PORT;

//MQTT Topics
const char* light_topic = LIGHT_DATA_TOPIC;
const char* moisture_topic = MOISTURE_DATA_TOPIC;
const char* temperature_topic = TEMPERATURE_DATA_TOPIC;
const char* humidity_topic = HUMIDITY_DATA_TOPIC;
const char* waterpump_activate_topic = WATERPUMP_ACTIVATE_TOPIC;
const char* waterpump_error_topic = WATERPUMP_ERROR_TOPIC;

//How often Sensor Data is sent
const long interval = INTERVAL_SEND;

//Arduino Board Configuration
const int LightDigital_Input = LIGHT_DIGITAL_INPUT;
const int LightAnalog_Input = LIGHT_ANALOG_INPUT;
const int WaterpumpDigital_Output = WATERPUMP_DIGITAL_OUTPUT;
const int MoistureAnalog_Input = MOISTURE_ANALOG_INPUT;
const int DHTPIN = TEMPERATURE_HUMIDITY_DIGITAL_INPUT;

//Temperature and Humidity Sensor
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

//WiFi and MQTT Client
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);

  while (!Serial)
    delay(10);

  setupWifiAndMQTT();
  //setup MQTT Message receiver
  setupMQTTReceiver();

  setupSensors();
}

void loop() {
  mqttClient.poll();
  readAndSendMeasurements();
  delay(interval);
}

void setupSensors() {
  pinMode(LightDigital_Input, INPUT);
  pinMode(LightAnalog_Input, INPUT);
  pinMode(WaterpumpDigital_Output, OUTPUT);
  pinMode(MoistureAnalog_Input, INPUT);
  dht.begin();
  
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

  while (!mqttClient.connect(mqtt_broker, mqtt_port)) {
    // MQTT connection failed, retry
    Serial.print("MQTT connection failed! Error code = ");
    Serial.print(mqttClient.connectError());
    Serial.println(". Retrying...");
    delay(2000);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void setupMQTTReceiver() {
  mqttClient.onMessage(onMqttMessage);
  Serial.print("Subscribing to topic: ");
  Serial.println(waterpump_activate_topic);
  mqttClient.subscribe(waterpump_activate_topic);
}

void readAndSendMeasurements() {
  int light_value = analogRead(LightAnalog_Input);
  float temperature_value = dht.readTemperature();
  float humidity_value = dht.readHumidity();
  float moisture_value = analogRead(MoistureAnalog_Input);

  moisture_value = calculateMoisture(moisture_value);

  Serial.print("Light Value: ");
  Serial.println(light_value);
  sendDataOverMQTT(light_value, light_topic);

  Serial.print("Moisture Value: (in %): ");
  Serial.println(moisture_value);
  sendDataOverMQTT(moisture_value, moisture_topic);

  Serial.print("Temperature Value(in °C): ");
  Serial.println(temperature_value);
  sendDataOverMQTT(temperature_value, temperature_topic);

  Serial.print("Humidity Value(in %rH): ");
  Serial.println(humidity_value);
  sendDataOverMQTT(humidity_value, humidity_topic);
}

//Max-Wert: 795
//Min-Wert: 370
float calculateMoisture(float moisture_value) {
  float moisture_percent = moisture_value - 370;
  moisture_percent = moisture_percent / 425 * 100;
  moisture_percent = 100 - moisture_percent;
  return moisture_percent;
}

void sendDataOverMQTT(int data, const char* topic) {
  Serial.print("Sending data to topic: ");
  Serial.println(topic);

  //send message, the Print interface can be used to set the message contents
  mqttClient.beginMessage(topic);
  mqttClient.print(data);
  mqttClient.endMessage();
}

void onMqttMessage(int messageSize) {
  Serial.println();
  Serial.print("Received a message with topic ");
  Serial.println(mqttClient.messageTopic());
  const char* received_topic = mqttClient.messageTopic().c_str();

  // Allocate a buffer to hold the incoming message
  char messageBuffer[messageSize + 1];  // +1 for null terminator
  memset(messageBuffer, 0, sizeof(messageBuffer));  // Clear the buffer

  // Read the message into the buffer
  int bytesRead = 0;
  while (mqttClient.available() && bytesRead < messageSize) {
    char c = mqttClient.read();
    messageBuffer[bytesRead] = c;
    bytesRead++;
  }

  // Null-terminate the buffer
  messageBuffer[bytesRead] = '\0';
  
  // Convert the message buffer to an integer
  int received_value = atoi(messageBuffer);

  // Now 'receivedValue' contains the integer value from the MQTT message
  Serial.print("Received value: ");
  Serial.println(received_value);

  if (strcmp(received_topic, waterpump_activate_topic) == 0) {
    Serial.println("Activating Waterpump.");
    activate_pump(&received_value);
  }
}

void activate_pump(int* waterpump_activation_time) {
  if (*waterpump_activation_time > 10) {
    *waterpump_activation_time = 10;
  }
  Serial.print("Waterpump pumping for ");
  Serial.print(*waterpump_activation_time);
  Serial.println(" seconds.");
  digitalWrite(WaterpumpDigital_Output, HIGH);
  delay(*waterpump_activation_time * 1000);
  digitalWrite(WaterpumpDigital_Output, LOW);
}

//Currently not in use
void sendWaterpumpError() {
  Serial.print("Sending data to topic: ");
  Serial.println(waterpump_error_topic);

  //send message, the Print interface can be used to set the message contents
  mqttClient.beginMessage(waterpump_error_topic);
  mqttClient.print(true);
  mqttClient.endMessage();
}