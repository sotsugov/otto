import time
from behave import *


# Then Steps
@then('the response is successful')
def step_impl(context):
    actual_status = context.response.status_code
    assert actual_status == 200, \
        f"Unexpected response status. Expected 200, actual {actual_status}"


@then("the response does not contain errors")
def step_impl(context):
    error_message = context.response.json()["error"]
    assert len(
        error_message) == 0, f"Response contains errors: {error_message}"


@then('latency is less than "{expected_latency:d}" ms')
def step_impl(context, expected_latency):
    time_server = context.response.json()["result"]["unixtime"]
    time_client = int(time.time())
    latency = time_client - time_server
    assert latency < expected_latency, \
        f"Expected latency <{expected_latency}, actual {latency}"


@then('the response result length is "{n_expected:d}"')
def step_impl(context, n_expected):
    n_actual = len(context.response.json()["result"])
    assert n_actual == n_expected, \
        f"Actual number of items in response received {n_actual}, does not match expected {n_expected}"


@then('the response result contains "{items}"')
def step_impl(context, items):
    expected_items = items.split(",")
    actual_items = context.response.json()["result"].keys()
    assert all(i in actual_items for i in expected_items), \
        f"Missing {items} from the response items: {actual_items}"


@then('the account balance is "{currency}" value "{value}"')
def step_impl(context, currency, value):
    result = context.response.json()['result']
    assert currency in result.keys(
    ), f"Missing currency {currency} in result {result.keys()}"
    assert result[currency] == value, f"Expected value {value}, does not match {result[currency]}"


@then('ensures order history is empty')
def step_impl(context):
    open_orders = context.response.json()['result']['open']
    assert len(
        open_orders) == 0, f"Expected open orders to be empty, received {open_orders}"


@then('ensures there are exactly "{number:d}" open orders')
def step_impl(context, number):
    open_orders = context.response.json()['result']['open']
    assert len(
        open_orders) == number, f"Expected number of open orders to be {number}, received {open_orders}"
