# Import necessary modules
from behave import given, when, then
from logic.mqtt_package.mqtt_subscriber import MQTTSubscriber

# Global variable to store the received topic
received_topic = None

@given("a set of valid topics")
def step_given_valid_topics(context):
    context.valid_topics = [
        "light_ard",
        "moisture_ard",
        "humidity_ard",
        "temperature_ard",
        "waterpump_error_ard",
    ]

@given("an unvalid topic")
def step_given_invalid_topic(context):
    context.invalid_topic = "invalid_topic"

@when("we receive a message with a valid topic")
def step_receive_valid_message(context):
    received_topic = context.valid_topics[0]
    message = "Valid message content"
    ArduinoDataProcessor.receive_message(received_topic, message)

@when("we receive a message with an unvalid topic")
def step_receive_invalid_message(context):
    received_topic = context.invalid_topic
    message = "Invalid message content"
    ArduinoDataProcessor.receive_message(received_topic, message)

@then("we will write the data into the right table")
def step_write_data_to_table(context):
    # Assuming a function `write_to_table` is available in ArduinoDataProcessor
    assert received_topic in context.valid_topics
    ArduinoDataProcessor.write_to_table(received_topic)

@then("we won't do anything")
def step_do_nothing(context):
    # Assuming a function `write_to_table` is available in ArduinoDataProcessor
    assert received_topic == context.invalid_topic
    ArduinoDataProcessor.write_to_table(received_topic)  # Here, the assumption is that this function won't perform any action for an invalid topic
