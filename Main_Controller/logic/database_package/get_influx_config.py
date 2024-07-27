import yaml
import os
from dotenv import load_dotenv

from ..mqtt_package.get_mqtt_config import get_table_names, get_topic_mapping

load_dotenv()

def get_influx_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'influx_config.yaml')
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        influxdb_config = data["influxdb_config"]

    token = os.environ.get("INFLUX_TOKEN")
    org = influxdb_config["org"]
    url = os.environ.get("INFLUX_URL")
    bucket = influxdb_config["bucket"]

    return token, org, url, bucket

def get_table_topics():
    table_names = get_table_names()
    return table_names

def get_table_mapping():
    table_map = get_topic_mapping()
    return table_map



