import paho.mqtt.client as mqtt
import yaml
import os

from influxdb_package.insert_data import write_data

dir_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
with open(yaml_path, 'r') as f:
    data = yaml.safe_load(f)
    mqtt_resources = data["mqtt_resources"]

broker_address = mqtt_resources["BROKER_ADDRESS"]
topics = [mqtt_resources["LIGHT_DATA_TOPIC"], mqtt_resources["MOISTURE_DATA_TOPIC"],mqtt_resources["HUMIDITY_DATA_TOPIC"], mqtt_resources["TEMPERATURE_DATA_TOPIC"], mqtt_resources["WATERPUMP_ERROR_TOPIC"]]
broker_port = mqtt_resources["BROKER_PORT"]

class MQTTSubscriber:
    def __init__(self):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.events = []

        # Set up the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in topics:
                client.subscribe(topic)
        else:
            print("Connection failed with code", rc)

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        print(f"Received message on topic '{message.topic}': {payload}")

        write_data(message.topic, payload)   

    def subscribe(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
