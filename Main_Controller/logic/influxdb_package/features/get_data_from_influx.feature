Feature: Retrieving Data from influx
    In order to find the right reactions to the status of the plant
    We need to regularly retrieve data from the database
    To work with more data we will get every minute the last 5 data_entries of the database

    Scenario: One minute is overnjjn
        Given it has been a minute since the last retrieval
        Then we will get the last 5 data_entries from InfluxDB