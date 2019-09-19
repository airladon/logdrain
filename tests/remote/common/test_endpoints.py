import json
import requests
import pytest  # noqa: F401
import os
from shutil import rmtree

# def test_root(address, auth):
#     r = json.loads(requests.get(f'{address}/', auth=auth).content)
#     assert r['status'] == 'ok'



def test_requires_authentication(address):
    r = requests.get(f'{address}/')
    assert r.status_code == 401


def test_root(get):
    r = get('/')
    assert r['status'] == 'ok'


def test_post(post):
    r = post('/dev', 'abcd')
    assert r.status_code == 200

# Test to make sure endpoint is user/pass protected
