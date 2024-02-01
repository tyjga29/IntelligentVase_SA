import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from .get_influx_config import get_table_topics, get_table_mapping, get_influx_config

from .DatabaseHandler_functions.helper_functions import insert_data, get_data

class DatabaseHandler:
    def __init__(self):
        self.table_mapping = get_table_mapping()
        self.table_names = get_table_topics()
           
        self.token, self.org, self.url, self.bucket = get_influx_config()

        self.influx_client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.influx_client.query_api()

    def write_data(self, topic, value):
        insert_data(self.write_api, self.bucket, self.org, self.table_mapping, topic, value)

    # Retrieves the mean of all the tables of the last minute
    def retrieve_data(self):
        tables = get_data(self.query_api, self.table_names, self.bucket, self.org)
        return tables
        