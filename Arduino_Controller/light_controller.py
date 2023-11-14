import paho.mqtt.client as mqtt
from mongo_db_controller import send_light_to_mongodb


broker_address = "mqtt_broker_address"  # Replace with your MQTT broker's address
port = 1883  # Replace with your MQTT broker's port
username = "mqtt_username"  # Replace with your MQTT username
password = "mqtt_password"  # Replace with your MQTT password
topic = "mqtt_topic"  # Replace with the topic you want to subscribe to

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    received_number = int(msg.payload.decode())
    send_light_to_mongodb(received_number)

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)
client.loop_forever()
