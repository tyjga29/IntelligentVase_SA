Scenario Outline: Moisture level <scenario_name>
    Given an intelligent vase which is ready to manage soil moisture
    And the vase holds a <plan_type>
    And that plant requires <optimal_level> as a moisture level
    When <average_moisture_level> is reached
    Then <expected_action> should have happened in the next 5 seconds
    Examples:
       |  scenario_name                  | plant_type  | optimal_level | average_moisture_level | expected_action | 
       |   Below optimal for succulent   | Cactus      | 10            | 5             	        | Activate Pump   | 
       |   Optimal for succulent         | Cactus      | 10            | 10            	        | Do Nothing      | 
       |   Too high for succulent        | Cactus      | 10            | 15            	        | Alert User      | 
       |   Below optimal for tomato      | Tomato      | 60            | 50            	        | Activate Pump   | 
       |   Optimal for tomato            | Tomato      | 60            | 60            	        | Do Nothing      | 
       |   Too high for tomato           | Tomato      | 60            | 70            	        | Alert User      | 