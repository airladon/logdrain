import json
import requests
import os
import pytest  # noqa: F401

app_name = os.environ.get('HEROKU_APP_NAME_OVERRIDE') or \
    'ENTER_APP_NAME_HERE'
address = f'https://{app_name}.herokuapp.com'


def test_root():
    r = json.loads(requests.get(f'{address}/').content)
    assert r['status'] == 'ok'
