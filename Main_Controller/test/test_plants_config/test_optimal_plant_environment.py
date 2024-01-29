import unittest
from logic.plants_config.optimal_plant_environment import OptimalPlant, get_optimal_plants_as_list
from logic.plants_config.optimal_plants_list_functions import get_optimal_plants_as_list, find_optimal_plant_by_name

class TestOptimalPlant(unittest.TestCase):
    def setUp(self):
        self.csv_row_tomato = ["Tomato", "15", "32", "65", "85", "immer leicht feucht", "3", "6", "direct"]
        self.csv_row_succulent = ["Succulent", "4", "27", "40", "50", "trocken", "120", "6", "shade", "Grows the best if it has constant, strong light. Should lay a bit in the shade. Be careful of direct sun. Ideally they should get a lot of air circulation."]
        self.csv_file_path = "logic/plants_config/plants.csv"
        self.optimal_plants = OptimalPlant.load_from_csv(self.csv_file_path)
        self.expected_tomato = ["Tomato", "15", "32", "65", "85", "immer leicht feucht", "3", "6", "direct", '']

    def test_initialization_tomato(self):
        optimal_plant = OptimalPlant(*self.csv_row_tomato)

        self.assertEqual(optimal_plant.plant, "Tomato")
        self.assertEqual(optimal_plant.temperature_min, 15)
        self.assertEqual(optimal_plant.temperature_max, 32)
        self.assertEqual(optimal_plant.humidity_min, 65)
        self.assertEqual(optimal_plant.humidity_max, 85)
        self.assertEqual(optimal_plant.moisture, "immer leicht feucht")
        self.assertEqual(optimal_plant.pause_for_watering, 3)
        self.assertEqual(optimal_plant.sun_min, 6)
        self.assertEqual(optimal_plant.sun_category, "direct")
        self.assertEqual(optimal_plant.notes, None)

    def test_initialization_succulent(self):
        optimal_plant = OptimalPlant(*self.csv_row_succulent)

        self.assertEqual(optimal_plant.plant, "Succulent")
        self.assertEqual(optimal_plant.temperature_min, 4)
        self.assertEqual(optimal_plant.temperature_max, 27)
        self.assertEqual(optimal_plant.humidity_min, 40)
        self.assertEqual(optimal_plant.humidity_max, 50)
        self.assertEqual(optimal_plant.moisture, "trocken")
        self.assertEqual(optimal_plant.pause_for_watering, 120)
        self.assertEqual(optimal_plant.sun_min, 6)
        self.assertEqual(optimal_plant.sun_category, "shade")
        self.assertEqual(optimal_plant.notes, "Grows the best if it has constant, strong light. Should lay a bit in the shade. Be careful of direct sun. Ideally they should get a lot of air circulation.")

    def test_from_csv_row_tomato(self):
        optimal_plant = OptimalPlant.from_csv_row(self.csv_row_tomato)

        self.assertEqual(optimal_plant.plant, "Tomato")
        self.assertEqual(optimal_plant.temperature_min, 15)
        self.assertEqual(optimal_plant.temperature_max, 32)
        self.assertEqual(optimal_plant.humidity_min, 65)
        self.assertEqual(optimal_plant.humidity_max, 85)
        self.assertEqual(optimal_plant.moisture, "immer leicht feucht")
        self.assertEqual(optimal_plant.pause_for_watering, 3)
        self.assertEqual(optimal_plant.sun_min, 6)
        self.assertEqual(optimal_plant.sun_category, "direct")
        self.assertEqual(optimal_plant.notes, None)

    def test_from_csv_row_succulent(self):
        optimal_plant = OptimalPlant.from_csv_row(self.csv_row_succulent)

        self.assertEqual(optimal_plant.plant, "Succulent")
        self.assertEqual(optimal_plant.temperature_min, 4)
        self.assertEqual(optimal_plant.temperature_max, 27)
        self.assertEqual(optimal_plant.humidity_min, 40)
        self.assertEqual(optimal_plant.humidity_max, 50)
        self.assertEqual(optimal_plant.moisture, "trocken")
        self.assertEqual(optimal_plant.pause_for_watering, 120)
        self.assertEqual(optimal_plant.sun_min, 6)
        self.assertEqual(optimal_plant.sun_category, "shade")
        self.assertEqual(optimal_plant.notes, "Grows the best if it has constant, strong light. Should lay a bit in the shade. Be careful of direct sun. Ideally they should get a lot of air circulation.")

    def test_load_from_csv(self):
        plants_data = [self.csv_row_tomato, self.csv_row_succulent]
        get_optimal_plants_as_list = lambda x: plants_data

        optimal_plants = OptimalPlant.load_from_csv(self.csv_file_path)

        self.assertEqual(optimal_plants[0].plant, "Tomato")
        self.assertEqual(optimal_plants[1].plant, "Succulent")

    def test_get_optimal_plants_as_list(self):
        plants_data = get_optimal_plants_as_list(self.csv_file_path)

        self.assertEqual(plants_data[0], self.expected_tomato)
        self.assertEqual(plants_data[1], self.csv_row_succulent)

    def test_find_optimal_plant_by_name_found(self):
        plant_name = "Tomato"
        found_plant = find_optimal_plant_by_name(self.optimal_plants, plant_name)

        self.assertIsNotNone(found_plant)
        self.assertEqual(found_plant.plant, "Tomato")

    def test_find_optimal_plant_by_name_not_found(self):
        plant_name = "NonexistentPlant"
        found_plant = find_optimal_plant_by_name(self.optimal_plants, plant_name)

        self.assertIsNone(found_plant)

if __name__ == '__main__':
    unittest.main()
