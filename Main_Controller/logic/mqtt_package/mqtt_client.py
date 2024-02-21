import logging
logger = logging.getLogger(__name__)

import paho.mqtt.client as mqtt

from .get_mqtt_config import get_mqtt_address_and_port, get_mqtt_subscriber_topics, get_mqtt_waterpump_activate_topic

class MQTTClient:
    def __init__(self, db_handler):
        self.broker_address, self.broker_port = get_mqtt_address_and_port()
        logging.debug(f"Initializing client with broker_address={self.broker_address} on broker_port={self.broker_port}")
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
            logging.info("Connected to MQTT broker")
            for topic in self.subscriber_topics:
                client.subscribe(topic)
                logging.debug("Subscribed to topic: %s", topic)
        else:
            logging.error("Connection failed with code %s", rc)

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        logging.info("Received message on topic '%s': %s", message.topic, payload)

        if self.db_handler:
            self.db_handler.write_data(message.topic, payload)
        else:
            logging.warning("InfluxDB is missing")

    def subscribe(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()
        logging.debug("MQTT Client subscribed and loop started")

    def activate_pump(self, waterpump_activation_in_s):
        logging.info("Activating pump for %s seconds.", waterpump_activation_in_s)
        message = str(waterpump_activation_in_s)
        self.client.publish(self.waterpump_activate_topic, message)
        logging.debug(f"Waterpump mqtt-signal successfully sent to topic={self.waterpump_activate_topic}")

    def stop(self):
        self.client.disconnect()
