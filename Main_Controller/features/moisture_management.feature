Feature: Moistuere Level Management
    Scenario Outline: Moisture level <scenario_name>
        Given an intelligent vase which is ready to manage soil moisture
        And the vase holds a <plant_type>
        And we have a list of optimal environment for plants where we can search the matching plant <plant_type>
        And that plant requires an optimal moisture level between <min_optimal_level> and <max_optimal_level>
        When the plant has an average moisture level of <average_moisture_level>
        Then <expected_action> should happen

        Examples:
            | scenario_name                  | plant_type | min_optimal_level | max_optimal_level | average_moisture_level | expected_action  |
            | Below optimal for succulent    | Succulent  | 8                 | 12                | 5                      | Activate Pump    |
            | Optimal for succulent          | Succulent  | 8                 | 12                | 10                     | Do Nothing       |
            | Too high for succulent         | Succulent  | 8                 | 12                | 15                     | Alert User       |
