Controller zwischen Arduino und Datenbank
5. - 6. Semester, Projektarbeit DHBW Stuttgart

This Controller receives information from an Arduino Uno WiFi R4 over MQTT, which will compare the data to database of several plants for controlling the environment of a pot

InDepth:
The script.py will start the mqtt_subscriber in the mqtt_package. The appropriate topics will be listened to and then the values will be used to send them over insert_data.py in the influxdb_package.

Use of docker:
Is something changed in the Main_Controller please delete the container in Docker Desktop. Then:
docker-compose build
docker-compose up -d

InfluxDB:
To log into InfluxDB use:
user: root
password: secret_password

Needed libraries:
    pymongo
    yaml
    paho.mqtt.client