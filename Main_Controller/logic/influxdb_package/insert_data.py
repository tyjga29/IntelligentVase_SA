import os, yaml
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from logic.mqtt_package.get_mqtt_config import get_topic_mapping
from logic.influxdb_package.get_influx_config import get_influx_config

#Get Topics from mqtt_resources.yaml
topic_mapping = get_topic_mapping()

#Get InfluxDB Configs from config.yaml
token, org, url , bucket= get_influx_config()
#Initialize Client
write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
def write_data(topic, value):
    measurement_name = None
    for topic_info in topic_mapping:
        if topic == topic_info["MQTT_TOPIC"]:
            measurement_name = topic_info["TABLE_NAME"]
            break
    
    if measurement_name is not None:
        value = float(value)
        point = (
            Point(measurement_name)
            .tag("SensorId", "1")
            .field("Measurement", value)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Sent data to datapoint: {measurement_name}")
    else:
        print("Unknown topic received")