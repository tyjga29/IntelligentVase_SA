from behave import given, when, then
import time

from logic.plants_config.plant_sensor_data.plant_sensor_data import PlantSensorData

@given("an intelligent vase which is ready to manage soil moisture")
def step_given_intelligent_vase(context):
    context.plant = PlantSensorData()
    pass

@given("the vase holds a {plant_type}")
def step_given_vase_holds_plant(context, plant_type):
    context.plant_type = plant_type

@given("that plant requires {optimal_level} as a moisture level")
def step_given_plant_requires_optimal_level(context, optimal_level):
    context.optimal_level = int(optimal_level)

@when("{average_moisture_level} is reached")
def step_when_average_moisture_level_reached(context, average_moisture_level):
    context.average_moisture_level = int(average_moisture_level)

@then("{expected_action} should have happened in the next 5 seconds")
def step_then_expected_action_in_next_5_seconds(context, expected_action):
    # Your test logic here
    time.sleep(5)  # Simulating the wait for 5 seconds
    assert context.expected_action == expected_action  # Add your actual assertion logic

# You may need additional steps based on your test logic
