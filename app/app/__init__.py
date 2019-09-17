from flask import Flask
from app.config import Config
from flask_talisman import Talisman
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
app.config.from_object(Config)
SELF = "'self'"
if not os.environ.get('LOCAL_PRODUCTION') \
   or os.environ.get('LOCAL_PRODUCTION') != 'DISABLE_SECURITY':
    talisman = Talisman(app)
auth = HTTPBasicAuth()

from app import routes  # noqa
