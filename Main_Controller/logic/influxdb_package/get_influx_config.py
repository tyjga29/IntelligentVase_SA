import yaml
import os

def get_influx_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'influx_config.yaml')
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        influxdb_config = data["influxdb_config"]

    token = influxdb_config["token"]
    org = influxdb_config["org"]
    url = influxdb_config["url"]
    bucket = influxdb_config["bucket"]

    return token, org, url, bucket

