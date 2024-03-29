import yaml
import os

from dotenv import load_dotenv

load_dotenv()

def load_mqtt_resources():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        mqtt_resources = data["mqtt_resources"]

    return mqtt_resources

def get_mqtt_address_and_port():
    broker_address = os.environ.get("MQTT_BROKER_ADDRESS")
    broker_port_str = os.environ.get("MQTT_BROKER_PORT")
    broker_port = int(broker_port_str)

    return broker_address, broker_port

def get_mqtt_subscriber_topics():
    mqtt_resources = load_mqtt_resources()
    subscriber_topics = [
        entry["MQTT_TOPIC"] for entry in mqtt_resources["SUBSCRIBER_TOPICS"]
    ]
    return subscriber_topics

def get_table_names():
    mqtt_resources = load_mqtt_resources()
    table_names = [
        entry["TABLE_NAME"] for entry in mqtt_resources["SUBSCRIBER_TOPICS"]
    ]
    return table_names

#Return all the Subscriber topics with their respecive Table names
def get_topic_mapping():
    mqtt_resources = load_mqtt_resources()
    topic_mapping = mqtt_resources["SUBSCRIBER_TOPICS"]
    return topic_mapping


# Function to get Waterpump sender topic
def get_mqtt_waterpump_activate_topic():
    mqtt_resources = load_mqtt_resources()
    waterpump_activate_topic = mqtt_resources.get("WATERPUMP_ACTIVATE_TOPIC", "")
    return waterpump_activate_topic