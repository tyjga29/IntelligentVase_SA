import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from logic.mqtt_package.mqtt_client import MQTTClient

class TestMQTTClient(unittest.TestCase):
    def setUp(self):
        # Create an instance of MQTTClient for testing
        self.mqtt_client = MQTTClient(None)

    def test_on_connect_successful(self):
        # Create a mock for the mqtt.Client
        mock_client = MagicMock()
        
        # Use patch to capture the printed output and replace the client with the mock
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
             patch.object(self.mqtt_client, 'client', mock_client):

            # Call the on_connect method with a successful connection
            self.mqtt_client.on_connect(mock_client, None, None, 0)

            # Get the printed output
            printed_output = mock_stdout.getvalue().strip()

        # Assert the printed output
        expected_output = "Connected to MQTT broker"
        self.assertEqual(printed_output, expected_output)

        # Assert that subscribe was called with all subscriber topics
        subscriber_topics = self.mqtt_client.subscriber_topics
        for topic in subscriber_topics:
            mock_client.subscribe.assert_any_call(topic)

    def test_on_connect_unsuccessful(self):
        # Create a mock for the mqtt.Client
        mock_client = MagicMock()
        
        # Use patch to capture the printed output and replace the client with the mock
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
             patch.object(self.mqtt_client, 'client', mock_client):

            # Call the on_connect method with an unsuccessful connection (e.g., rc=1)
            self.mqtt_client.on_connect(mock_client, None, None, 1)

            # Get the printed output
            printed_output = mock_stdout.getvalue().strip()

        # Assert the printed output
        expected_output = "Connection failed with code 1"
        self.assertEqual(printed_output, expected_output)

    def test_on_message(self):
        # Simulate an incoming message
        test_topic = "light_ard"
        test_payload = b"30"
        message = MagicMock()
        message.topic = test_topic
        message.payload.decode.return_value = test_payload

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.mqtt_client.on_message(None, None, message)

            printed_output = mock_stdout.getvalue().strip()

        expected_output = f"Received message on topic '{test_topic}': {test_payload}"
        expected_output += "\nInfluxDB is missing"
        self.assertEqual(printed_output, expected_output)

    def test_activate_pump(self):
        self.mqtt_client.activate_pump(10)

        # Simulate some delay to allow the thread to execute
        import time
        time.sleep(1)

    def tearDown(self):
        # Clean up resources if needed
        self.mqtt_client.stop()

if __name__ == '__main__':
    unittest.main()

