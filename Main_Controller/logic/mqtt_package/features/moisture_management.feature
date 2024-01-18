Feature: Water Pump Activation
  In order to regulate the moisture of the plant's soil
  I want the pump to only activate 
  When the moisture level is too far below the optimal level

  Scenario: Moisture Level too low
    Given the optimal moisture level is 50%
    When the actual moisture level is 20%
    Then the pump is activated for 5 seconds

  Scenario: Moisture Level optimal or Above
    Given the optimal moisture level is 50%
    When the actual moisture level is <moisture>
    Then we won't do anything

    Examples:
      | moisture |
      | 45%      |
      | 50%      |
      | 60%      |


