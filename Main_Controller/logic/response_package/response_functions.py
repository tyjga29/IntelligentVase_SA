import logging
logger = logging.getLogger(__name__)

activation_time_pump = 3

def moisture_response(matching_plant, real_plant, mqtt_client):
    actual_moisture = real_plant.moisture
    moisture_min = matching_plant.moisture_min
    moisture_max = matching_plant.moisture_max

    if actual_moisture > moisture_max:
        logging.info(f"Soil Moisture {actual_moisture} % is higher than recommended value={moisture_max}. Please put the plant inside or take it into the sun for a short time to dry.")
    elif actual_moisture < moisture_min:
        logging.info(f"Soil Moisture {actual_moisture} % is lower than recommended value={moisture_min}. Activating waterpump.")
        mqtt_client.activate_pump(activation_time_pump)
    else:
        logging.info("Soil Moisture adequate.")