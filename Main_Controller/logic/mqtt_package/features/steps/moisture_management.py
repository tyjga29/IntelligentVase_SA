from behave import given, when, then

from logic.mqtt_package.mqtt_waterpump_sender import activate_pump

@given('the moisture level is way too low')
def moisture_too_low(context):
    context.moisture_level = 5

@when('I activate the pump')
def activate_pump(context):
    # code to activate the pump and adjust moisture level
    context.moisture_level = activate_pump(7)

@then('the moisture level should reach the desired level')
def check_desired_level(context):
    assert context.moisture_level == 7, "Moisture level did not reach the desired level"

@given('the moisture level is the same, slightly above or under the desired level')
def moisture_near_desired(context):
    context.moisture_level = 7

@then("I don't do anything")
def do_nothing(context):
    pass

@given('the moisture level is way too high')
def moisture_too_high(context):
    context.moisture_level = 15

@then('I notify the user')
def notify_user(context):
    # Code to notify the user
    context.user_notified = True

