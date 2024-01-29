import unittest
import tempfile
import os
import yaml
from logic.mqtt_package.get_mqtt_config import load_mqtt_resources, get_mqtt_address_and_port, get_mqtt_subscriber_topics, get_table_names, get_topic_mapping, get_mqtt_waterpump_activate_topic

class TestGetMqttConfig(unittest.TestCase):

    def setUp(self):
        # Create a temporary YAML file for testing
        self.test_yaml_content = """
        mqtt_resources:
          BROKER_ADDRESS: "test.mosquitto.org"
          BROKER_PORT: 1883
          SUBSCRIBER_TOPICS:
            - MQTT_TOPIC: "light_ard"
              TABLE_NAME: "light"
            - MQTT_TOPIC: "moisture_ard"
              TABLE_NAME: "moisture"
            - MQTT_TOPIC: "humidity_ard"
              TABLE_NAME: "humidity"
            - MQTT_TOPIC: "temperature_ard"
              TABLE_NAME: "temperature"
            - MQTT_TOPIC: "waterpump_error_ard"
              TABLE_NAME: "waterpump_error"
          WATERPUMP_ACTIVATE_TOPIC: "waterpump_activate_ard"
        """

        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write(self.test_yaml_content)
        self.temp_file.close()

    def tearDown(self):
        # Remove the temporary YAML file
        os.remove(self.temp_file.name)

    def test_yaml_content_match(self):
        # Check if the actual content of the temporary YAML file matches the expected content
        with open(self.temp_file.name, 'r') as f:
            actual_yaml_content = f.read()

        self.assertEqual(actual_yaml_content, self.test_yaml_content)

    def test_load_mqtt_resources(self):
        # Test if the function loads the YAML file correctly
        result = load_mqtt_resources()
        self.assertEqual(result['BROKER_ADDRESS'], "test.mosquitto.org")
        self.assertEqual(result['BROKER_PORT'], 1883)
        self.assertIn('SUBSCRIBER_TOPICS', result)
        self.assertEqual(result['WATERPUMP_ACTIVATE_TOPIC'], "waterpump_activate_ard")

    def test_get_mqtt_address_and_port(self):
        # Test if the function returns the correct address and port
        address, port = get_mqtt_address_and_port()
        self.assertEqual(address, "test.mosquitto.org")
        self.assertEqual(port, 1883)

    def test_get_mqtt_subscriber_topics(self):
        # Test if the function returns the correct subscriber topics
        result = get_mqtt_subscriber_topics()
        expected_topics = ["light_ard", "moisture_ard", "humidity_ard", "temperature_ard", "waterpump_error_ard"]
        self.assertEqual(result, expected_topics)

    def test_get_table_names(self):
        # Test if the function returns the correct table names
        result = get_table_names()
        expected_table_names = ["light", "moisture", "humidity", "temperature", "waterpump_error"]
        self.assertEqual(result, expected_table_names)

    def test_get_topic_mapping(self):
        # Test if the function returns the correct topic mapping
        result = get_topic_mapping()
        expected_mapping = [
            {"MQTT_TOPIC": "light_ard", "TABLE_NAME": "light"},
            {"MQTT_TOPIC": "moisture_ard", "TABLE_NAME": "moisture"},
            {"MQTT_TOPIC": "humidity_ard", "TABLE_NAME": "humidity"},
            {"MQTT_TOPIC": "temperature_ard", "TABLE_NAME": "temperature"},
            {"MQTT_TOPIC": "waterpump_error_ard", "TABLE_NAME": "waterpump_error"}
        ]
        self.assertEqual(result, expected_mapping)

    def test_get_mqtt_waterpump_activate_topic(self):
        # Test if the function returns the correct waterpump activate topic
        result = get_mqtt_waterpump_activate_topic()
        self.assertEqual(result, "waterpump_activate_ard")

if __name__ == '__main__':
    unittest.main()
