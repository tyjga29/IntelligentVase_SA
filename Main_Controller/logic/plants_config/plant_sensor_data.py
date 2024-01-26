from ..influxdb_package.database_handler import DatabaseHandler

class PlantSensorData:
    def __init__(self, temperature, light, humidity, moisture):
        self.temperature = temperature
        self.humidity = humidity
        self.light= light
        self.moisture = moisture

    #TODO here we should be able to just parse the values from Influx into the calss
    @classmethod
    def get_current_values():
        DatabaseHandler.retrieve_data()
        print("Help")