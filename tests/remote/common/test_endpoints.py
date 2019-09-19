import requests
import pytest  # noqa: F401


def test_requires_authentication(address, authentication):
    r = requests.get(f'{address}/')
    assert r.status_code == 401

    r = requests.get(f'{address}/', auth=authentication)
    assert r.status_code == 200


def test_root(get):
    r = get('/')
    assert r['status'] == 'ok'


def test_post(post):
    r = post('/dev', 'abcd')
    assert r.status_code == 200
