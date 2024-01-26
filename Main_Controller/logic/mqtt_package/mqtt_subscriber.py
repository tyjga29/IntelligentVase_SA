import paho.mqtt.client as mqtt

from .get_mqtt_config import get_mqtt_address_and_port, get_mqtt_subscriber_topics
from ..influxdb_package.database_handler import DatabaseHandler

broker_address, broker_port = get_mqtt_address_and_port()
subscriber_topics = get_mqtt_subscriber_topics()

class MQTTSubscriber:
    def __init__(self, db_handler):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.events = []
        self.db_handler = db_handler

        # Set up the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in subscriber_topics:
                client.subscribe(topic)
        else:
            print("Connection failed with code", rc)

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        print(f"Received message on topic '{message.topic}': {payload}")

        if self.db_handler:
            self.db_handler.write_data(message.topic, payload)
        else:
            print("InfluxDB is missing")

    def subscribe(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
