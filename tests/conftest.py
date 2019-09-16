import pytest  # noqa: F401
import os
import sys
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, './app/')
from app import app  # noqa

# Remember, if database changes have happened, need to copy the new
# app.db to tests/flask/test_app.db


@pytest.fixture(scope="module")
def client(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'app_test.db')
    # app.config['MAIL_USERNAME'] = ''

    client = app.test_client()

    yield client

    # def fin():
    #     print('unload stuff here')
    # request.addfinalizer(fin)
