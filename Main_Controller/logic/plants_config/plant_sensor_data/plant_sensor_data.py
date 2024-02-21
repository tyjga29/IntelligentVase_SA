import logging
logger = logging.getLogger(__name__)

from datetime import datetime

class PlantSensorData:
    def __init__(self, temperature, light, humidity, moisture, current_time):
        self.temperature = temperature
        self.humidity = humidity
        self.light= light
        self.moisture = moisture
        self.current_time = current_time

    @classmethod
    def get_current_values(cls, database_handler):
        try:
            tables = database_handler.retrieve_data()
            if tables is not None:
                temperature = None
                light = None
                humidity = None
                moisture = None
                # Parse the data from tables
                for table in tables:
                    if table is not None:
                        for record in table.records:
                            if record is not None:
                                measurement = record.get_measurement()
                                field_value = record.get_value()
                                logging.debug(f"Measurement: {measurement}")
                                logging.debug(f"Field Value: {field_value}")

                                if measurement == 'temperature':
                                    temperature = field_value
                                elif measurement == 'light':
                                    light = field_value
                                elif measurement == 'humidity':
                                    humidity = field_value
                                elif measurement == 'moisture':
                                    moisture = field_value

                current_time = datetime.now()
                # Create an instance of PlantSensorData
                data = cls(temperature, light, humidity, moisture, current_time)
                logging.info(f"Plant environment: Time: {data.current_time}, Temperature: {data.temperature}, Light: {data.light}, Humidity: {data.humidity}, Moisture: {data.moisture}")
                return data
            else:
                logging.warning("Tables are empty")
                return None

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return None