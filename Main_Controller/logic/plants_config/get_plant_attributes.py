import yaml

attributes_file = "Main_Controller/logic/plants_config/plants_attributes.yaml"

def get_plants_columns_mapping():
    try:
        with open(attributes_file, 'r') as yaml_file:
            plant_attributes = yaml.safe_load(yaml_file)
            return plant_attributes
    except Exception as e:
        # Handle exceptions, print an error message, or return an empty list as needed
        print(f"Error: {e}")
        return []
    
def get_plant_attributes():
    try:
        with open(attributes_file, 'r') as file:
            data = yaml.safe_load(file)

        # Extracting values only
        values = list(data.values())

        return values
    except Exception as e:
        # Handle exceptions, print an error message, or return an empty list as needed
        print(f"Error: {e}")
        return []