import json
import requests
import os
import pytest  # noqa: F401
# from yaml import safe_load
# from pathlib import Path

# # addresses = safe_load(Path().absolute() / '..' / '..' / 'app.yml')
# # print(addresses)
# yml_file = (Path().absolute() / 'addresses.yml').absolute().as_posix()
# addresses = {}
# with open(yml_file, 'r') as f:
#     addresses = safe_load(f)

# address = os.environ.get('HEROKU_ADDRESS')


def test_root():
    address = os.environ.get('HEROKU_ADDRESS')
    assert address is not None
    r = json.loads(requests.get(f'{address}/').content)
    assert r['status'] == 'ok'
