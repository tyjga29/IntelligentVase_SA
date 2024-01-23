import pandas as pd
import json

file_path = "Main_Controller/logic/plants_config/plants.csv"

def import_plants_from_csv():
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

        if df.empty:
            raise ValueError("The DataFrame is empty. No data to process.")

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
        return plants_json

    except Exception as e:
        # Handle exceptions, print an error message, or return an empty list as needed
        print(f"Error: {e}")
        return []