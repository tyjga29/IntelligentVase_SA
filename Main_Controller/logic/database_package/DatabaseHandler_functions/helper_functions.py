from influxdb_client import Point

def insert_data(influx_write_api, influx_bucket, influx_org, table_mapping, table_topic, value):
    measurement_name = None
    for topic_info in table_mapping:
        if table_topic == topic_info["MQTT_TOPIC"]:
            measurement_name = topic_info["TABLE_NAME"]
            break
    
    tag = "SensorId"
    tag_nr = "1"
    field = "Measurement"

    if measurement_name is not None:
        value = float(value)
        point = (
            Point(measurement_name)
            .tag(tag, tag_nr)
            .field(field, value)
        )
        influx_write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        print(f"Sent value {value} to datapoint: {measurement_name} on tag {tag} with the number {tag_nr} and the field {field}")
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