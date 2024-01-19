from influxdb_client import Point

def insert_data(self, topic, value):
    measurement_name = None
    for topic_info in self.table_mapping:
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
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        print(f"Sent data to datapoint: {measurement_name}")
    else:
        print("Unknown topic received")