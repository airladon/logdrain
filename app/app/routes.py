from flask import jsonify, request
from app import app, auth
import os
from app.tools import add_to_log


@app.route('/')
@auth.login_required
def home():
    return jsonify({'status': 'ok'})


@auth.verify_password
def verify_password(username, password):
    if os.environ.get('LOCAL_PRODUCTION') and \
       os.environ.get('LOCAL_PRODUCTION') == 'DISABLE_SECURITY':
        return True
    if username != os.environ.get('LOG_APP_USERNAME'):
        return False
    if password != os.environ.get('LOG_APP_PASSWORD'):
        return False
    return True


@app.route('/dev', methods=['GET', 'POST'])
@auth.login_required
def log_dev():
    add_to_log('dev', request.data.decode('utf-8'))
    return ''


@app.route('/test', methods=['GET', 'POST'])
@auth.login_required
def log_test():
    add_to_log('test', request.data.decode('utf-8'))
    return ''


@app.route('/log', methods=['GET', 'POST'])
@auth.login_required
def log_prod():
    add_to_log('prod', request.data.decode('utf-8'))
    return ''
