Controller zwischen Arduino und Datenbank
5. - 6. Semester, Projektarbeit DHBW Stuttgart

This Controller receives information from an Arduino Uno WiFi R4 over MQTT, which will compare the data to database of several plants for controlling the environment of a pot

InDepth:
The script.py will start the mqtt_subscriber in the mqtt_package. The appropriate topics will be listened to and then the values will be used to send them over insert_data.py in the datahandler_package.

We use a .env file for secrets

Use of docker:
Is something changed in the Main_Controller please run from that directory:
docker-compose build
docker-compose up -d

InfluxDB:
To log into InfluxDB use:
user: root
password: secret_password

Virtual environment:
To install librarys: pip install -r requirements.txt
To save changes: pip freeze > requirements.txt

Unittests:
To run all unittests execute in the Main_Controller:
    python -m unittest
To run unittests run the specific test from the Main_Controller with this command:
    python -m unittest test_mqtt_subscriber.py
