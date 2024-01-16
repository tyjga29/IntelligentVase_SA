Feature: Moisture Management

  Scenario: Responding to Moisture Levels

    Given the moisture level is way too low
      When I activate the pump
      Then the moisture level should reach the desired level

    Given the moisture level is the same or slightly above or under the desired level
      Then I don't do anything

    Given the moisture level is way too high
      Then I notify the user