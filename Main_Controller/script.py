import threading

from influxdb_client.client.write_api import SYNCHRONOUS

from logic.mqtt_package.mqtt_client import MQTTClient
from logic.response_package.response_handler import ResponseHandler
from logic.database_package.database_handler import DatabaseHandler
from logic.plants_config.optimal_plants.optimal_plant_environment import OptimalPlant
from logic.plants_config.plant_sensor_data.plant_sensor_data import PlantSensorData

#TODO database of plants with the id of the arduino
plant_name = "Succulent"

def calculation_thread(database_handler, response_handler):
    while True:
        try:
            optimal_plants = OptimalPlant.load_from_csv()
            real_plant = PlantSensorData.get_current_values(database_handler)
            response_handler.judge_environemnt(optimal_plants, real_plant, plant_name)
            threading.Event().wait(60)

        except ValueError as ve:
            print(f"Error : {ve}")
            threading.Event().wait(60)
        except Exception as e:
            print(f"An unexpected error occured: {e}")
            threading.Event().wait(60)

if __name__ == "__main__":
    # Create an instance of the MQTTSubscriber class
    database_handler = DatabaseHandler()
    mqtt_client = MQTTClient(database_handler)
    response_handler = ResponseHandler(mqtt_client)

    #MQTT Subscriber Thread
    subscriber_thread = threading.Thread(target=mqtt_client.subscribe)
    subscriber_thread.start()

    #Database Handler Thread
    database_handler_thread = threading.Thread(target=calculation_thread, args=(database_handler, response_handler))
    database_handler_thread.start()

    try:
        while True:
            # We can perform other tasks here while the client is subscribed
            pass
    except KeyboardInterrupt:
        mqtt_client.stop()
        database_handler_thread.join()