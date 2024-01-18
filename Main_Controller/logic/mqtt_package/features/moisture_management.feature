Feature: Moisture Management

  Scenario: Water Pump Activation
    Given the moisture level is too low
    When we activate the pump
    Then the pump should run for 5 seconds

  Scenario Outline: Moisture at Perfect Level or Above
    Given the moisture level is <moisture>
    When we check the moisture level
    Then we should not activate the pump

    Examples:
      | moisture |
      | 100%     |
      | 95%      |
      | 105%     |
