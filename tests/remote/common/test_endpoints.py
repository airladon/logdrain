import json
import requests
import pytest  # noqa: F401
import os


def test_root(address):
    r = json.loads(requests.get(
        f'{address}/',
        auth=(os.environ.get('LOG_USERNAME'), os.environ.get('LOG_PASSWORD'))
    ).content)
    assert r['status'] == 'ok'
