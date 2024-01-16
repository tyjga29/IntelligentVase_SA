import paho.mqtt.publish as publish

from .get_mqtt_config import get_mqtt_address_and_port, get_mqtt_waterpump_activate_topic

broker_address, broker_port = get_mqtt_address_and_port()
topic = get_mqtt_waterpump_activate_topic

def activate_pump(desired_moisture_level):
    publish.single(topic, desired_moisture_level, hostname=broker_address, port=broker_port)