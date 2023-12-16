import influxdb_client, os, time, yaml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#Get Topics from mqtt_resources.yaml
dir_path = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(dir_path, os.pardir))
yaml_path = os.path.join(project_root, 'mqtt_package', 'mqtt_resources.yaml')
with open(yaml_path, 'r') as f:
    data = yaml.safe_load(f)
    mqtt_resources = data["mqtt_resources"]
topics = [
    mqtt_resources["LIGHT_DATA_TOPIC"],
    mqtt_resources["MOISTURE_DATA_TOPIC"],
    mqtt_resources["WATERPUMP_ERROR_TOPIC"]
]

token = "secret_token"
org = "my_org"
url = "http://influxdb:8086"

write_client = InfluxDBClient(url=url, token=token, org=org)

bucket= "my_bucket"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
def write_data(topic, value):
    measurement_name = ""

    if topic == mqtt_resources["LIGHT_DATA_TOPIC"]:
        measurement_name = "light"
    elif topic == mqtt_resources["MOISTURE_DATA_TOPIC"]:
        measurement_name = "moisture"
    elif topic == mqtt_resources["WATERPUMP_ERROR_TOPIC"]:
        measurement_name = "pump_error"
    else:
        # Handle unknown topics, if needed
        pass

    if measurement_name:
        value = float(value)
        point = (
            Point(measurement_name)
            .tag("SensorId", "1")
            .field("Measurement", value)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Sent data to datapoint: {measurement_name}")
