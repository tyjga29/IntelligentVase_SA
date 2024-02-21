import logging
logger = logging.getLogger(__name__)

from logic.plants_config.optimal_plants.optimal_plants_list_functions import find_optimal_plant_by_name
from logic.mqtt_package.mqtt_client import MQTTClient
from logic.response_package.response_functions import moisture_response

class ResponseHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    def judge_environemnt(self, optimal_plants, real_plant, plant_name):
        matching_plant = find_optimal_plant_by_name(optimal_plants, plant_name)

        logging.info("Comparing sensor data with optimal values")
        moisture_response(matching_plant, real_plant, self.mqtt_client)
        
        # Check temperature conditions
        #if actual_temperature < matching_plant.temperature_min:
        #    print(f"Temperature of {actual_temperature} °C is too low. Please rise to at least {matching_plant.temperature_min}.")
        #elif actual_temperature > matching_plant.temperature_max:
        #    print(f"Temperature of {actual_temperature} °C is too high. Please drop to at max {matching_plant.temperature_max}.")
        #else:
        #    print("Temperature adequate.")
        
        # Check moisture conditions
        


        