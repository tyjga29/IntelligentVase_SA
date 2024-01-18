import paho.mqtt.publish as publish
import threading

from .get_mqtt_config import get_mqtt_address_and_port, get_mqtt_waterpump_activate_topic

broker_address, broker_port = get_mqtt_address_and_port()
topic = get_mqtt_waterpump_activate_topic

def activate_pump(waterpump_activation_in_s):
    message = str(waterpump_activation_in_s)
    
    #Seperate Thread for the MQTT Client Loop
    threading.Thread(target=publish.single, args=(topic, message), kwargs={"hostname": broker_address, "port": broker_port}).start()