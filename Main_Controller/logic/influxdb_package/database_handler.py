from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .get_influx_config import get_table_topics, get_table_mapping, get_influx_config

from .DatabaseHandler_functions.insert_data import insert_data

class DatabaseHandler:
    def __init__(self):
        self.table_mapping = get_table_mapping()
        self.table_names = get_table_topics()
           
        self.token, self.org, self.url, self.bucket = get_influx_config()

        self.influx_client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.influx_client.query_api()
    
    def write_data(self, topic, value):
        insert_data(self, topic, value)

    # Retrieves the mean of all the tables in the last minute
    def retrieve_data(self):
        print("Trying to retrieve Data from InfluxDB")
        try:
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
                else:
                    raise Exception(f"Error: No entries found in table {table_name}")

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")