Feature: Received MQTT Data
    In order to parse received information from the Arduino
    Into the right table in the database
    We need to differentiate between valid and unvalid topics
    We also need to differentiate between different valid topics

    Scenario: A valid topic is Given
        Given a set of valid topics
        | valid topic         |
        | light_ard           | 
        | moisture_ard        |
        | humidity_ard        |
        | temperature_ard     |
        | waterpump_error_ard |
        When we receive a message with a valid topic
        Then we will write the data into the right table
    
    Scenario: A unvalid topic is Given
        Given an unvalid topic
        When we receive a message with an unvalid topic
        Then we won't do anything
