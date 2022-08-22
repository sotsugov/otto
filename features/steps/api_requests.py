import base64
import hashlib
import hmac
import urllib
import time
import requests
from behave import *


# Given Steps
@given('I query public API "{endpoint}" endpoint')
def step_impl(context, endpoint):
    context.uri_path = f"/0/public/{endpoint}"


@given('I query private API "{endpoint}" endpoint')
def step_impl(context, endpoint):
    context.uri_path = f'/0/private/{endpoint}'


@given('I request the "{pair}" asset pair')
def step_impl(context, pair):
    context.params = {}
    context.params["pair"] = pair


@given('I am an authenticated user')
def step_impl(context):
    context.data = {}
    context.data["nonce"] = int(1000 * time.time())
    if context.global_data['api_otp']:
        context.data["otp"] = context.global_data['api_otp']

    post_data = urllib.parse.urlencode(context.data)
    encoded = (str(context.data["nonce"]) + post_data).encode()
    message = context.uri_path.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(
        context.global_data['api_secret']), message, hashlib.sha512)
    sig_digest = base64.b64encode(mac.digest())

    context.headers = {
        "API-Key": context.global_data['api_key'],
        "API-Sign": sig_digest.decode()
    }


# When Steps
@when('I make a request')
def step_impl(context):
    context.url = context.global_data["api_url"] + context.uri_path
    context.data = getattr(context, 'data', None)
    context.params = getattr(context, 'params', None)
    context.headers = getattr(context, 'headers', None)
    context.response = requests.post(
        context.url, data=context.data, headers=context.headers, params=context.params)
