import pytest  # noqa
import os
import json
import requests

test_address = os.environ.get('LOG_APP_TEST_ADDRESS')
prod_address = os.environ.get('LOG_APP_PROD_ADDRESS')
dev_address = os.environ.get('LOG_APP_DEV_ADDRESS')
local_address = 'http://host.docker.internal:5003'

auth = (os.environ.get('LOG_APP_USERNAME'), os.environ.get('LOG_APP_PASSWORD'))
server_value = 'no_server'


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="dev")


def get_dev_request(endpoint):
    return json.loads(
        requests.get(f'{dev_address}{endpoint}', auth=auth).content)


def get_test_request(endpoint):
    return json.loads(
        requests.get(f'{test_address}{endpoint}', auth=auth).content)


def get_prod_request(endpoint):
    return json.loads(
        requests.get(f'{prod_address}{endpoint}', auth=auth).content)


def get_local_request(endpoint):
    return json.loads(
        requests.get(f'{local_address}{endpoint}', auth=auth).content)


def post_dev_request(endpoint, data):
    return json.loads(requests.post(
        url=f'{dev_address}{endpoint}', auth=auth, data=data).content)


def post_test_request(endpoint, data):
    return json.loads(
        requests.post(f'{dev_address}{endpoint}', auth=auth).content)


def post_prod_request(endpoint, data):
    return json.loads(
        requests.post(f'{test_address}{endpoint}', auth=auth).content)


def post_local_request(endpoint, data):
    return requests.post(f'{local_address}{endpoint}', auth=auth, data=data)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    server_value = metafunc.config.option.server
    if 'address' in metafunc.fixturenames:
        if server_value == 'prod':
            metafunc.parametrize("address", [prod_address])
        if server_value == 'test':
            metafunc.parametrize("address", [test_address])
        if server_value == 'dev':
            metafunc.parametrize("address", [dev_address])
        if server_value == 'local':
            metafunc.parametrize("address", [local_address])
    if 'get' in metafunc.fixturenames:
        if server_value == 'prod':
            metafunc.parametrize("get", [get_prod_request])
        if server_value == 'test':
            metafunc.parametrize("get", [get_test_request])
        if server_value == 'dev':
            metafunc.parametrize("get", [get_dev_request])
        if server_value == 'local':
            metafunc.parametrize("get", [get_local_request])
    if 'post' in metafunc.fixturenames:
        if server_value == 'prod':
            metafunc.parametrize("post", [post_prod_request])
        if server_value == 'test':
            metafunc.parametrize("post", [post_test_request])
        if server_value == 'dev':
            metafunc.parametrize("post", [post_dev_request])
        if server_value == 'local':
            metafunc.parametrize("post", [post_local_request])


# @pytest.fixture
# def auth():
#     return (
#         os.environ.get('LOG_APP_USERNAME'), os.environ.get('LOG_APP_PASSWORD'))
