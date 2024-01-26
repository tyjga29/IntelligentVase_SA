import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from logic.mqtt_package.mqtt_subscriber import MQTTSubscriber

class TestMQTTSubscriber(unittest.TestCase):
    def setUp(self):
        # Create an instance of MQTTSubscriber for testing
        self.mqtt_subscriber = MQTTSubscriber(None)

    def test_on_message(self):
        # Simulate an incoming message
        test_topic = "light_ard"
        test_payload = b"30"
        message = MagicMock()
        message.topic = test_topic
        message.payload.decode.return_value = test_payload

        # Use patch to capture the printed output
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            # Call the on_message method with the mocked message
            self.mqtt_subscriber.on_message(None, None, message)

            # Get the printed output
            printed_output = mock_stdout.getvalue().strip()

        # Assert the printed output
        expected_output = f"Received message on topic '{test_topic}': {test_payload}"
        expected_output += "\nInfluxDB is missing"
        self.assertEqual(printed_output, expected_output)

    def tearDown(self):
        # Clean up resources if needed
        self.mqtt_subscriber.stop()

if __name__ == '__main__':
    unittest.main()

