import os, yaml
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from logic.mqtt_package.get_mqtt_config import get_mqtt_subscriber_topics
from logic.influxdb_package.get_influx_config import get_influx_config

#Get Topics from mqtt_resources.yaml
mqtt_topics = get_mqtt_subscriber_topics

#Get InfluxDB Configs from config.yaml
token, org, url = get_influx_config()

write_client = InfluxDBClient(url=url, token=token, org=org)

bucket= "my_bucket"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
def write_data(topic, value):
    measurement_name = ""

    #TODO very clunky
    if topic == mqtt_topics["LIGHT_DATA_TOPIC"]:
        measurement_name = "light"
    elif topic == mqtt_topics["MOISTURE_DATA_TOPIC"]:
        measurement_name = "moisture"
    elif topic == mqtt_topics["HUMIDITY_DATA_TOPIC"]:
        measurement_name = "humidity"
    elif topic == mqtt_topics["TEMPERATURE_DATA_TOPIC"]:
        measurement_name = "temperature"
    elif topic == mqtt_topics["WATERPUMP_ERROR_TOPIC"]:
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
