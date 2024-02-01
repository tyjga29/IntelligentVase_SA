from behave import given, when, then

import io
from contextlib import redirect_stdout

from datetime import datetime

from logic.plants_config.plant_sensor_data.plant_sensor_data import PlantSensorData
from logic.database_package.database_handler import DatabaseHandler
from logic.mqtt_package.mqtt_client import MQTTClient
from logic.plants_config.optimal_plants.optimal_plant_environment import OptimalPlant
from logic.plants_config.optimal_plants.optimal_plants_list_functions import find_optimal_plant_by_name
from logic.response_package.response_functions import moisture_response

@given("an intelligent vase which is ready to manage soil moisture")
def step_given_intelligent_vase(context):
    temperature_value = 25.0
    light_value = 500
    humidity_value = 60.0
    moisture_value = 35
    current_time_value = datetime.now()

    context.plant = PlantSensorData(temperature_value, light_value, humidity_value, moisture_value, current_time_value)

@given("the vase holds a {plant_type}")
def step_given_vase_holds_plant(context, plant_type):
    context.plant_type = plant_type

@given("we have a list of optimal environment for plants where we can search the matching plant {plant_type}")
def step_given_plant_requires_optimal_level(context, plant_type):
    optimal_plants = OptimalPlant.load_from_csv()
    context.matching_plant = find_optimal_plant_by_name(optimal_plants, plant_type)

@given("that plant requires an optimal moisture level between {min_optimal_level:d} and {max_optimal_level:d}")
def step_given_plant_requires_optimal_level(context, min_optimal_level, max_optimal_level):
    context.matching_plant.moisture_min = min_optimal_level
    context.matching_plant.moisture_max = max_optimal_level

@when("the plant has an average moisture level of {average_moisture_level}")
def step_at_certain_average_moisture(context, average_moisture_level):
    context.plant.moisture = float(average_moisture_level)

@then("{expected_action} should happen")
def step_then_expected_action(context, expected_action):
    database_handler = DatabaseHandler()
    context.mqtt_client = MQTTClient(context)

    captured_output = io.StringIO()
    with redirect_stdout(captured_output):
        moisture_response(context.matching_plant, context.plant, context.mqtt_client)
    print_output = captured_output.getvalue()

    print(f"this is the printed output: {print_output}")
    
    if expected_action.lower() == "alert user":
        assert print_output.lower(), f"Soil Moisture {context.plant.moisture} % is too high. Please put the plant inside or take it into the sun for a short time to dry."
    elif expected_action.lower() == "activate pump":
        assert print_output.lower(), f"Soil Moisture {context.plant.moisture} % is too low. Activating waterpump."
    elif expected_action.lower() == "do nothing":
        assert print_output.lower(), f"Soil Moisture adequate."

