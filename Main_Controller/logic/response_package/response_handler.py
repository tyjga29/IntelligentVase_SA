import json

from ..plants_config.optimal_plants_list_functions import find_optimal_plant_by_name

class ResponseHandler:
    def __init__(self):
        test = "test"
    def judge_environemnt(self, plant_data, optimal_plants, plant_name):
        matching_plant = find_optimal_plant_by_name(optimal_plants, plant_name)