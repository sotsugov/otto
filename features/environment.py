from behave import fixture, use_fixture
import os


@fixture
def read_api_url(context):
    # Attempt to read api url from environment variables before making any API calls
    context.global_data = {}
    context.global_data["api_url"] = os.environ.get("OTTO_URL", "")

    if not context.global_data["api_url"]:
        raise Exception(
            "API url is not provided, terminating. Make sure OTTO_URL has been set.")


@fixture
def read_keys(context):
    context.global_data["api_key"] = os.environ.get("OTTO_KEY", "")
    context.global_data["api_secret"] = os.environ.get("OTTO_SECRET", "")
    context.global_data["api_otp"] = os.environ.get("OTTO_OTP", "")

    # Not raising an exception here if the keys are not present,
    # we might want to check that the api returns an error when unauthorised
    # requests are being made


def before_all(context):
    use_fixture(read_api_url, context)


def before_tag(context, tag):
    if tag == 'private_api':
        use_fixture(read_keys, context)
