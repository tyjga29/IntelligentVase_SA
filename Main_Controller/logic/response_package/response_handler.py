from logic.plants_config.optimal_plants.optimal_plants_list_functions import find_optimal_plant_by_name
from logic.mqtt_package.mqtt_client import MQTTClient

activation_time_pump = 3

class ResponseHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    def judge_environemnt(self, optimal_plants, real_plant, plant_name):
        matching_plant = find_optimal_plant_by_name(optimal_plants, plant_name)
        actual_temperature = real_plant.temperature
        actual_moisture = real_plant.moisture
        
        # Check temperature conditions
        if actual_temperature < matching_plant.temperature_min:
            print(f"Temperature of {actual_temperature} °C is too low. Please rise to at least {matching_plant.temperature_min}.")
        elif actual_temperature > matching_plant.temperature_max:
            print(f"Temperature of {actual_temperature} °C is too high. Please drop to at max {matching_plant.temperature_max}.")
        else:
            print("Temperature adequate.")
        
        # Check moisture conditions
        if actual_moisture > matching_plant.moisture_max:
            print(f"Soil Moisture {actual_moisture} % is too high. Please put the plant inside or take it into the sun for a short time to dry.")
        elif actual_moisture < matching_plant.moisture_min:
            print(f"Soil Moisture {actual_moisture} % is too low. Activating waterpump.")
            self.mqtt_client.activate_pump(activation_time_pump)
        else:
            print("Soil Moisture adequate.")


        