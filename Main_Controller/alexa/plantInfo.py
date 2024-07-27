import json

from logic.plants_config.plant_sensor_data.plant_sensor_data import PlantSensorData

def lambda_handler(event, context):
    request_type = event['request']['type']
    
    if request_type == 'LaunchRequest':
        return on_launch(event)
    elif request_type == 'IntentRequest':
        return on_intent(event)
    elif request_type == 'SessionEndedRequest':
        return on_session_ended(event)

def on_launch(event):
    return build_response("Welcome to Plant Info. You can ask me about your plant's status.")

def on_intent(event):
    intent_name = event['request']['intent']['name']
    
    if intent_name == 'PlantInfoIntent':
        return get_plant_info()
    elif intent_name == 'AMAZON.HelpIntent':
        return build_response("You can ask for information about your plant by saying, give me information about my plant.")
    elif intent_name in ['AMAZON.CancelIntent', 'AMAZON.StopIntent']:
        return build_response("Goodbye!")
    else:
        return build_response("Sorry, I don't know that one.")

def on_session_ended(event):
    return build_response("Goodbye!")

def get_plant_info():
    real_plant = PlantSensorData.get_current_values(database_handler)

    temperature = str(real_plant.temperature)
    soil_moisture = str(real_plant.humidity)
    humidity = str(real_plant.light)
    sunlight = str(real_plant.moisture)
    
    plant_info = (
        f"Your plant needs the following conditions: "
        f"Temperature: {temperature} degree Celsius, "
        f"Soil Moisture: {soil_moisture} percent, "
        f"Humidity: {humidity} percent, and "
        f"Sunlight: {sunlight} lumen."
    )
    
    return build_response(plant_info)

def build_response(output_speech):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output_speech,
            },
            'shouldEndSession': True
        }
    }
