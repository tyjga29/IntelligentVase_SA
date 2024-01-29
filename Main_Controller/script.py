import threading

from logic.mqtt_package.mqtt_client import MQTTClient
from logic.influxdb_package.database_handler import DatabaseHandler
from logic.response_package.response_handler import ResponseHandler
from logic.plants_config.optimal_plants.optimal_plant_environment import OptimalPlant
from logic.plants_config.plant_sensor_data.plant_sensor_data import PlantSensorData

#TODO database of plants with the id of the arduino
plant_name = "Succulent"

def calculation_thread(database_handler, optimal_plants, calculator):
    while True:
        try:
            real_plant = PlantSensorData.get_current_values()
            influxdb_data = database_handler.retrieve_data()
            if (influxdb_data is None):
                raise ValueError("Values from InfluxDB cannot be None")
            ResponseHandler.judge_environemnt(influxdb_data, optimal_plants, plant_name)
            threading.Event().wait(60)

        except ValueError as ve:
            print(f"Error : {ve}")
        except Exception as e:
            print(f"An unexpected error occured: {e}")

        
if __name__ == "__main__":
    optimal_plants = OptimalPlant.load_from_csv()

    # Create an instance of the MQTTSubscriber class
    database_handler = DatabaseHandler()
    subscriber = MQTTClient(database_handler)
    
    #calculator = Calculator()

    #MQTT Subscriber Thread
    subscriber_thread = threading.Thread(target=subscriber.subscribe)
    subscriber_thread.start()

    #Database Handler Thread
    database_handler_thread = threading.Thread(target=calculation_thread, args=(database_handler, optimal_plants, None))
    database_handler_thread.start()

    try:
        while True:
            # We can perform other tasks here while the client is subscribed
            pass
    except KeyboardInterrupt:
        subscriber.stop()
        database_handler_thread.join()