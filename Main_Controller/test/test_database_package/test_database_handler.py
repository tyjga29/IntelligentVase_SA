import unittest
import threading
from io import StringIO
from unittest.mock import patch
from influxdb_client import InfluxDBClient
from logic.database_package.DatabaseHandler_functions.helper_functions import insert_data
from logic.database_package.get_influx_config import get_table_mapping

#TODO mock influxdb
class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        # Set up the InfluxDB client for testing with placeholder data
        self.table_mapping = get_table_mapping()

        self.token = 'fake_token'
        self.org = 'fake_organization'
        self.url = 'http://localhost:8086'
        self.bucket = 'fake_bucket'

        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api()

    def tearDown(self):
        # Clean up resources after each test
        threading.Thread._cleanup
        self.client.close()

    @patch('sys.stdout', new_callable=StringIO)
    def test_insert_data_valid_topic(self, mock_stdout):
        topic = "temperature_ard"
        value = 42.5
        insert_data(self.write_api, self.bucket, self.org, self.table_mapping, topic, value)

        expected_message = "Sent value 42.5 to datapoint: temperature on tag SensorId with the number 1 and the field Measurement\n"
        self.assertEqual(mock_stdout.getvalue(), expected_message)

        

if __name__ == '__main__':
    unittest.main()

