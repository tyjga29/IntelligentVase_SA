from behave import given, when, then
from assertpy import assert_that

from logic.mqtt_package.mqtt_waterpump_sender import activate_pump

@given('the optimal moisture level is {optimal_moisture}')
def step_given_optimal_moisture(context, optimal_moisture):
    context.optimal_moisture = float(optimal_moisture.rstrip('%'))

@when('the actual moisture level is {actual_moisture}')
def step_when_actual_moisture(context, actual_moisture):
    context.actual_moisture = float(actual_moisture.rstrip('%'))

@then('the pump is activated')
def step_then_pump_activated(context):
    assert_that(context.actual_moisture).is_less_than(context.optimal_moisture)
    activate_pump(context.activation_time)

@then('we won\'t do anything')
def step_then_nothing(context):
    assert_that(context.actual_moisture).is_greater_than_or_equal_to(context.optimal_moisture)
    # No pump activation