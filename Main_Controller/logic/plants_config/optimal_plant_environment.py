import csv

csv_file_path = "Main_Controller/logic/plants_config/plants.csv"

class OptimalPlant:
    def __init__(self, plant, temperature_min, temperature_max, humidity_min, humidity_max, moisture, pause_for_watering, sun_min, sun_category, notes):
        self.plant = plant
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.moisture = moisture
        self.pause_for_watering = pause_for_watering
        self.sun_min = sun_min
        self.sun_category = sun_category
        self.notes = notes

    @classmethod
    def from_csv_row(cls, csv_row):
        return cls(*csv_row)
    
    @classmethod
    def load_from_csv(cls):
        plants = []
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            header = next(reader)  # Skip the header row
            for row in reader:
                plant = cls.from_csv_row(row)
                plants.append(plant)
        return plants