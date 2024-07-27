import os

from .optimal_plants_list_functions import get_optimal_plants_as_list

dir_path = os.path.dirname(__file__)
csv_file_path = os.path.join(dir_path, "optimal_plants.csv")

class OptimalPlant:
    def __init__(self, plant, temperature_min, temperature_max, humidity_min, humidity_max, moisture_min, moisture_max, pause_for_watering, sun_min, sun_category, notes=None):
        self.plant = plant
        self.temperature_min = int(temperature_min)
        self.temperature_max = int(temperature_max)
        self.humidity_min = int(humidity_min)
        self.humidity_max = int(humidity_max)
        self.moisture_min = int(moisture_min)
        self.moisture_max = int(moisture_max)
        self.pause_for_watering = int(pause_for_watering)
        self.sun_min = int(sun_min)
        self.sun_category = sun_category
        self.notes = notes

    @classmethod
    def from_csv_row(cls, csv_row):
        return cls(*csv_row)
    
    @classmethod
    def load_from_csv(cls, file_path=csv_file_path):
        plants_data = get_optimal_plants_as_list(file_path)
        plants = [cls.from_csv_row(row) for row in plants_data]
        return plants