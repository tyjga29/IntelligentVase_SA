import pandas as pd
import json

from .get_plant_attributes import get_plants_columns_mapping

plant_mapping = get_plants_columns_mapping()

file_path = "Main_Controller/logic/plants_config/plants.csv"

def import_plants_from_csv():
    print("Trying to import the comparison plants data from the csv file")
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

        if df.empty:
            raise ValueError("The Plants DataFrame is empty. No data to process.")

        plants_data_list = []

        # Loop through the DataFrame
        for index, row in df.iterrows():
            plant_data = {}

            for header in df.columns:
                key = header
                value = row[header]
                plant_data[key] = value

            plants_data_list.append(plant_data)

        # Convert the JSON strings to Python objects
        plants_json = json.dumps(plants_data_list, ensure_ascii=False, indent=2)
        
        plants_json = change_mapping(plants_json)

        print("Plants from csv successfully imported")
        return plants_json

    except Exception as e:
        # Handle exceptions, print an error message, or return an empty list as needed
        print(f"Error: {e}")
        return []
    
def change_mapping(plants_json):
    print("Remapping comparison-plants-table")
    data = json.loads(plants_json)

    for obj in data:
        for old_attr, new_attr in plant_mapping.items():
            obj[new_attr] = obj.pop(old_attr, None)

    return json.dumps(data, indent=2)
