def find_optimal_plant_by_name(optimal_plants, plant_name):
    for plant in optimal_plants:
        if plant.plant.lower() == plant_name.lower():
            return plant
    return None  # Return None if the plant is not found