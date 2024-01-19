Feature: Moisture Management for different plants
    To keep the plant alive
    We need to make sure the soil has the optimal level of soil
    The level depends on the plant
    If it deviates from the optimal we take action

    Scenario: Moisture levels management for various plants
        Given the system is ready to manage soil moisture

        Examples:
            | Plant Type | Optimal Moisture Level | Mean Moisture Level | Action           |
            | Cactus      | 10                      | 5                   | Activate Pump     |  # Below optimal for cactus
            | Cactus      | 10                      | 10                  | Do Nothing        |  # Optimal for cactus
            | Cactus      | 10                      | 15                  | Alert User        |  # Too high for cactus

            | Tomato      | 60                      | 50                  | Activate Pump     |  # Below optimal for tomato
            | Tomato      | 60                      | 60                  | Do Nothing        |  # Optimal for tomato
            | Tomato      | 60                      | 70                  | Alert User        |  # Too high for tomato
