import unittest
from logic.mqtt_package.get_mqtt_config import get_mqtt_subscriber_topics

class TestGetMQTTConfig(unittest.TestCase):
    def test_get_mqtt_subscriber_topics(self):
        # Call the function
        subscriber_topics = get_mqtt_subscriber_topics()

        # Assert that the result is a list with exactly 5 entries
        self.assertEqual(len(subscriber_topics), 5)