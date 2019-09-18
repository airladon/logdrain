import pytest  # noqa
import os

test_address = os.environ.get('LOG_APP_TEST_ADDRESS')
prod_address = os.environ.get('LOG_APP_PROD_ADDRESS')
dev_address = os.environ.get('LOG_APP_DEV_ADDRESS')


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="dev")


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
