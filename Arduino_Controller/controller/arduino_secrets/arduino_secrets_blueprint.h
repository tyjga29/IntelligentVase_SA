#ifndef ARDUINO_SECRETS.h
#define ARDUINO_SECRETS.h

#define SECRET_SSID "your_wifi_ssid"
#define SECRET_PASS "your_wifi_password"

#define MQTT_BROKER "your_mqtt_broker"
#define MQTT_PORT 1883

#define LIGHT_DATA_TOPIC "your_light_topic"
#define MOISTURE_DATA_TOPIC "your_moisture_topic"
#define TEMPERATURE_DATA_TOPIC "temperature_ard"
#define HUMIDITY_DATA_TOPIC "humidity_ard"
#define WATERPUMP_ACTIVATE_TOPIC "waterpump_activate_topic"
#define WATERPUMP_ERROR_TOPIC "waterpump_error_topic"

#define INTERVAL_SEND 30000

#define LIGHT_DIGITAL_INPUT 0
#define LIGHT_ANALOG_INPUT 0
#define WATERPUMP_DIGITAL_OUTPUT 0
#define MOISTURE_ANALOG_INPUT 0
#define TEMPERATURE_HUMIDITY_DIGITAL_INPUT 0

#endif