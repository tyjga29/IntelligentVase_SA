Feature: Write data to Influx database
    To work with the data from the plant
    We first need to save it to the Influx Database
    Here we have to save the right info in the right table 

    Scenario: Received data with valid topic
        Given the system is ready to receive MQTT data
        When data with a valid topic is received from MQTT
        Then the information is matched to the right table in Influx
        And the data is written into the corresponding Influx table

        Examples:
            | Valid Topic          |
            | light_ard            |
            | moisture_ard         |
            | humidity_ard         |
            | temperature_ard      |
            | waterpump_error_ard  |

    Scenario: Invalid topic
        Given the system is ready to receive MQTT data
        When data with an invalid topic is received from MQTT
        Then an error is sent
        And the information is not saved in Influx

        Examples:
            | Invalid Topic        |
            | invalid_topic        |
            | unknown_topic        |
            | incorrect_topic      |