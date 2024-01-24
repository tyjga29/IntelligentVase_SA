import threading
from logic.mqtt_package.mqtt_subscriber import MQTTSubscriber
from logic.influxdb_package.database_handler import DatabaseHandler
from logic.plants_config.plants_config_handler import import_plants_from_csv

def calculation_thread(database_handler, calculator):
    while True:
        data = database_handler.retrieve_data()
        #calculator.perform_calculations(data)
        threading.Event().wait(60)

if __name__ == "__main__":
    import_plants_from_csv()

    # Create an instance of the MQTTSubscriber class
    subscriber = MQTTSubscriber()
    database_handler = DatabaseHandler()
    #calculator = Calculator()

    #MQTT Subscriber Thread
    subscriber_thread = threading.Thread(target=subscriber.subscribe)
    subscriber_thread.start()

    #Database Handler Thread
    database_handler_thread = threading.Thread(target=calculation_thread, args=(database_handler, None))
    database_handler_thread.start()

    try:
        while True:
            # We can perform other tasks here while the client is subscribed
            pass
    except KeyboardInterrupt:
        subscriber.stop()
        database_handler_thread.join()