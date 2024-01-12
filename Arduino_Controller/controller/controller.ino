#include <ArduinoMqttClient.h>
#include <WiFiS3.h>
#include "Adafruit_SHT4x.h"

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
Adafruit_SHT4x sht4 = Adafruit_SHT4x();

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
  setupSHT4();
  
}

void setupSHT4() {
  Serial.println("Trying to connect to Adafruit SHT4x:");
  /*while (!sht4.begin()) {
    Serial.println("Couldn't find SHT4x");
    delay(3000);
  }

  Serial.println("Found SHT4x sensor");
  Serial.print("Serial number 0x");
  Serial.println(sht4.readSerial(), HEX);

  // You can have 3 different precisions, higher precision takes longer
  sht4.setPrecision(SHT4X_HIGH_PRECISION);
  switch (sht4.getPrecision()) {
     case SHT4X_HIGH_PRECISION: 
       Serial.println("High precision");
       break;
     case SHT4X_MED_PRECISION: 
       Serial.println("Med precision");
       break;
     case SHT4X_LOW_PRECISION: 
       Serial.println("Low precision");
       break;
  }

  // You can have 6 different heater settings
  // higher heat and longer times uses more power
  // and reads will take longer too!
  sht4.setHeater(SHT4X_NO_HEATER);
  switch (sht4.getHeater()) {
     case SHT4X_NO_HEATER: 
       Serial.println("No heater");
       break;
     case SHT4X_HIGH_HEATER_1S: 
       Serial.println("High heat for 1 second");
       break;
     case SHT4X_HIGH_HEATER_100MS: 
       Serial.println("High heat for 0.1 second");
       break;
     case SHT4X_MED_HEATER_1S: 
       Serial.println("Medium heat for 1 second");
       break;
     case SHT4X_MED_HEATER_100MS: 
       Serial.println("Medium heat for 0.1 second");
       break;
     case SHT4X_LOW_HEATER_1S: 
       Serial.println("Low heat for 1 second");
       break;
     case SHT4X_LOW_HEATER_100MS: 
       Serial.println("Low heat for 0.1 second");
       break;
  }*/
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
  int moisture_value = analogRead(MoistureAnalog_Input);
  //sensors_event_t humidity, temp;   //SHT4x values
  //sht4.getEvent(&humidity, &temp);  //populate temp and humidity ;

  Serial.print("Light Value: ");
  Serial.println(light_value);
  sendDataOverMQTT(light_value, light_topic);

  Serial.print("Moisture Value: ");
  Serial.println(moisture_value);
  sendDataOverMQTT(moisture_value, moisture_topic);

  Serial.print("Temperature Value(in °C): ");
  Serial.println(temp.temperature);
  sendDataOverMQTT(temp.temperature, temperature_topic);

  Serial.print("Humidity Value(in %rH): ");
  Serial.println(humidity.relative_humidity);
  sendDataOverMQTT(humidity.relative_humidity, humidity_topic);
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