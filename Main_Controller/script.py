from mqtt_package.mqtt_subscriber import MQTTSubscriber

if __name__ == "__main__":
    # Create an instance of the MQTTSubscriber class
    subscriber = MQTTSubscriber()

    subscriber.subscribe()

    try:
        while True:
            # You can perform other tasks here while the client is subscribed
            pass
    except KeyboardInterrupt:
        subscriber.stop()