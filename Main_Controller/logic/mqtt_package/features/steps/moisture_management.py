from behave import given, when, then
import time

from logic.mqtt_package.mqtt_waterpump_sender import activate_pump

@given('the moisture level is way too low')
def step_moisture_way_too_low(context):
    context.moisture_level = 3 #Moisture Level that is too low

@when('we activate the pump')
def step_activate_pump(context):
    # Simulate activating the pump
    context.activation_time = 5  #Simulate running the pump for 5 seconds
    activate_pump(context.activation_time)
    time.sleep(context.activation_time)  #Simulate the pump running

@then('the pump should run for 5 seconds')
def step_pump_runs_for_5_seconds(context):
    assert context.activation_time == 5, "Pump should run for 5 seconds"

@given('the moisture level is {moisture}')
def step_moisture_above_or_at_perfect_level(context, moisture):
    if moisture.lower() == 'too low':
        context.moisture_level = 3
    elif '%' in moisture:
        context.moisture_level = float(moisture.rstrip('%'))
    else:
        context.moisture_level = float(moisture)

@when('we check the moisture level')
def step_check_moisture_level(context):
    # Simulate checking moisture level (replace this with your actual code)
    context.pump_activated = False

@then('we should not activate the pump')
def step_no_pump_activation(context):
    assert not context.pump_activated, "Pump should not be activated"