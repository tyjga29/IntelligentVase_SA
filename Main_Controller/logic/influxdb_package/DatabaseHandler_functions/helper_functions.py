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

#TODO this doesn't work right now I need to find a way to automatically put the sensorData into the class PlantSensorData
def get_data(self):
    print("Trying to retrieve Data from InfluxDB")
    try:
        temperature = None
        light = None
        humidity = None
        moisture = None

        # Construct and execute queries for each table
        for table_name in self.table_names:
            query = f"""from(bucket: "{self.bucket}")
                |> range(start: -1m)
                |> filter(fn: (r) => r._measurement == "{table_name}")
                |> mean()"""

            # Execute query
            tables = self.query_api.query(query, org=self.org)

            # Check if there are any records
            if tables and tables[0].records:
                # Print the results
                for table in tables:
                    for record in table.records:
                        print(record)
                
                return tables
                
            else:
                raise Exception(f"Error: No entries found in table {table_name}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")