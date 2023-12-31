#include <ArduinoMqttClient.h>
#include <WiFiS3.h>

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
const char* waterpump_activate_topic = WATERPUMP_ACTIVATE_TOPIC;
const char* waterpump_error_topic = WATERPUMP_ERROR_TOPIC;

//How often Sensor Data is send
const long interval = INTERVAL_SEND;

//ARduino Board Configuration
const int LightDigital_Input = LIGHT_DIGITAL_INPUT;
const int LightAnalog_Input = LIGHT_ANALOG_INPUT;
const int WaterpumpDigital_Output = WATERPUMP_DIGITAL_OUTPUT;
const int MoistureAnalog_Input = MOISTURE_ANALOG_INPUT;

//Waterpump Controller, how long to pump, pause between pumps, and how many times to do it in a row
const int waterpump_activation = WATERPUMP_ACTIVATION;
const int waterpump_pause = WATERPUMP_PAUSE;
const int waterpump_tries = WATERPUMP_TRIES;
const int moisture_margin_of_error = MOISTURE_MARGIN;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);

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
    delay(5000);
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
  int moisture_value = analogRead(MoistureAnalog_Input);

  Serial.print("Light Value: ");
  Serial.println(light_value);
  sendDataOverMQTT(light_value, light_topic);

  Serial.print("Moisture Value: ");
  Serial.println(moisture_value);
  sendDataOverMQTT(moisture_value, moisture_topic);
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
    activate_pump_to_moisture_level(received_value);
  }
}

void activate_pump_to_moisture_level(int value_to_reach) {
  bool level_reached = false;
  int error = 0;
  int beginning_moisture_level = analogRead(MoistureAnalog_Input);
  while (!level_reached) {
    int moisture_value = analogRead(MoistureAnalog_Input);
    if (error >= waterpump_tries) {
      if (moisture_value <= (beginning_moisture_level + moisture_margin_of_error)) {
        Serial.println("Error. Waterpump not working.");
        level_reached = true;
        sendWaterpumpError();
      }
      else {
        error = 0;
        beginning_moisture_level = moisture_value;
      }
    }
    else if (moisture_value < value_to_reach) {
      Serial.print("Waterpump pumping for ");
      Serial.print(waterpump_activation);
      Serial.println(" seconds.");

      digitalWrite(WaterpumpDigital_Output, HIGH);
      delay(5000);  //5 Seconds
      digitalWrite(WaterpumpDigital_Output, LOW);

      error = error + 1;
      Serial.print("Trying ");
      Serial.print(waterpump_tries - error);
      Serial.println(" more times.");

      delay(10000); //10 Seconds
    }
    else {
      Serial.println("Sufficient Moisture Level.");
      level_reached = true;
    }
  }
}

void sendWaterpumpError() {
  Serial.print("Sending data to topic: ");
  Serial.println(waterpump_error_topic);

  //send message, the Print interface can be used to set the message contents
  mqttClient.beginMessage(waterpump_error_topic);
  mqttClient.print(true);
  mqttClient.endMessage();
}