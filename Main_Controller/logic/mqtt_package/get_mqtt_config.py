import yaml
import os

def get_mqtt_address_and_port():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        mqtt_resources = data["mqtt_resources"]

    broker_address = mqtt_resources["BROKER_ADDRESS"]
    broker_port = mqtt_resources["BROKER_PORT"]

    return broker_address, broker_port

def get_mqtt_subscriber_topics():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        mqtt_resources = data["mqtt_resources"]

    topics = [
        mqtt_resources["LIGHT_DATA_TOPIC"],
        mqtt_resources["MOISTURE_DATA_TOPIC"],
        mqtt_resources["HUMIDITY_DATA_TOPIC"],
        mqtt_resources["TEMPERATURE_DATA_TOPIC"],
        mqtt_resources["WATERPUMP_ERROR_TOPIC"]
    ]

    return topics

# Function to get Waterpump sender topic
def get_mqtt_waterpump_activate_topic():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        mqtt_resources = data["mqtt_resources"]

    sender_topics = [
        mqtt_resources["WATERPUMP_ACTIVATE_TOPIC"],
    ]

    return sender_topics
