import paho.mqtt.client as mqtt
import threading

from .get_mqtt_config import get_mqtt_address_and_port, get_mqtt_subscriber_topics, get_mqtt_waterpump_activate_topic

class MQTTClient:
    def __init__(self, db_handler):
        self.broker_address, self.broker_port = get_mqtt_address_and_port()
        self.client = mqtt.Client()
        self.events = []
        self.db_handler = db_handler
        self.subscriber_topics = get_mqtt_subscriber_topics()
        self.waterpump_activate_topic = get_mqtt_waterpump_activate_topic()

        # Set up the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in self.subscriber_topics:
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

    def activate_pump(self, waterpump_activation_in_s):
        print(f"Activating pump for {waterpump_activation_in_s} seconds.")
        message = str(waterpump_activation_in_s)
        self.client.publish(self.waterpump_activate_topic, message)
        #threading.Thread(target=self.client.publish, args=(self.waterpump_activate_topic, message)).start()
        print("Waterpump mqtt-signal successfully sent.")

    def stop(self):
        self.client.disconnect()
