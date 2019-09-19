import pytest  # noqa
import os
import json
import requests

address = {
    'test': os.environ.get('LOG_APP_TEST_ADDRESS'),
    'prod': os.environ.get('LOG_APP_PROD_ADDRESS'),
    'dev': os.environ.get('LOG_APP_DEV_ADDRESS'),
    'local': 'http://host.docker.internal:5003',
}

auth = (os.environ.get('LOG_APP_USERNAME'), os.environ.get('LOG_APP_PASSWORD'))
server_value = 'no_server'


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="dev")


def get(endpoint, address):
    return json.loads(requests.get(f'{address}{endpoint}', auth=auth).content)


def post(endpoint, address, data):
    return requests.post(f'{address}{endpoint}', auth=auth, data=data)


get_request = {
    'local': lambda endpoint: get(endpoint, address['local']),
    'dev': lambda endpoint: get(endpoint, address['dev']),
    'test': lambda endpoint: get(endpoint, address['test']),
    'prod': lambda endpoint: get(endpoint, address['prod']),
}

post_request = {
    'local': lambda endpoint, data: post(endpoint, address['local'], data),
    'dev': lambda endpoint, data: post(endpoint, address['dev'], data),
    'test': lambda endpoint, data: post(endpoint, address['test'], data),
    'prod': lambda endpoint, data: post(endpoint, address['prod'], data),
}


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    server_value = metafunc.config.option.server
    if 'address' in metafunc.fixturenames:
        metafunc.parametrize("address", [address[server_value]])
    if 'get' in metafunc.fixturenames:
        metafunc.parametrize("get", [get_request[server_value]])
    if 'post' in metafunc.fixturenames:
        metafunc.parametrize("post", [post_request[server_value]])


# @pytest.fixture
# def auth():
#     return (
#         os.environ.get('LOG_APP_USERNAME'), os.environ.get('LOG_APP_PASSWORD'))
