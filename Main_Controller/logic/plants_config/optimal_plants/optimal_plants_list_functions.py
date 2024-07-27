import logging
logger = logging.getLogger(__name__)

import csv

def get_optimal_plants_as_list(csv_file_path):
    plants_data = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)
        for row in reader:
            plants_data.append(row)
    return plants_data

def find_optimal_plant_by_name(optimal_plants, plant_name):
    logging.debug(f"Searching for plant '{plant_name}'.")
    for plant in optimal_plants:
        if plant.plant.lower() == plant_name.lower():
            return plant
    logging.warning("No plant with the name has been found.")
    return None  # Return None if the plant is not found