import unittest

from logic.plants_config.optimal_plants_list_functions import get_optimal_plants_as_list
from logic.plants_config.optimal_plants_list_functions import find_optimal_plant_by_name

csv_file_path = "logic/plants_config/plants.csv"

#TODO Klasse testen
class TestOptimalPlantsListFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.optimal_plant_instance = get_optimal_plants_as_list(csv_file_path)

    def test_find_optimal_plant_by_name_existing(self):
        plant_name = "Tomato"
        result = find_optimal_plant_by_name(self.optimal_plant_instance, plant_name)
        self.assertIsNotNone(result)
        self.assertEqual(result.plant, plant_name)

    def test_find_optimal_plant_by_name_non_existing(self):
        # Test when the plant doesn't exist in the list
        plant_name = "Nonexistent Plant"
        result = find_optimal_plant_by_name(self.optimal_plant_instance, plant_name)
        self.assertIsNone(result)

    def test_find_optimal_plant_by_name_case_insensitive(self):
        # Test case-insensitive search
        plant_name = "sUccuLent"
        result = find_optimal_plant_by_name(self.optimal_plant_instance, plant_name)
        self.assertIsNotNone(result)
        self.assertEqual(result.plant.lower(), plant_name.lower())

if __name__ == '__main__':
    unittest.main()
