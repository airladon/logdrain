from flask import jsonify, request
from app import app, auth
import re
import os
import boto3
from datetime import datetime
from datetime import timezone

log_file = '/opt/app/log.txt'


def write_file(area, file_path, file_name):
    log_storage_address = os.environ.get('LOG_STORAGE_ADDRESS')
    region = re.search(
        r'\.([^\.]*)\.digitaloceanspaces.com$',
        log_storage_address).groups()[0]
    log_storage_access_key = os.environ.get('LOG_STORAGE_ACCESS_KEY')
    log_storage_secret = os.environ.get('LOG_STORAGE_SECRET_ACCESS_KEY')
    session = boto3.session.Session()
    client = session.client(
        's3',
        region_name=region,
        endpoint_url=log_storage_address,  # noqa
        aws_access_key_id=log_storage_access_key,
        aws_secret_access_key=log_storage_secret,
    )
    client.upload_file(log_file, area, file_name)


@app.route('/')
@auth.login_required
def home():
    return jsonify({'status': 'ok'})


def add_to_log(path):
    with open(log_file, 'a+') as f:
        f.write(request.data.decode('utf-8'))
    if os.path.isfile(log_file) and os.path.getsize(log_file) > 50000:
        write_to_space(path)
        with open(log_file, 'w') as f:
            f.write('')


def write_to_space(path):
    now = datetime.now(timezone.utc)
    dt_string = now.strftime("%Y.%m.%d-%H.%M.%S.%f")
    file_name = f'{dt_string}.txt'
    write_file('dev', '/opt/app', file_name)


@auth.verify_password
def verify_password(username, password):
    if os.environ.get('LOCAL_PRODUCTION') and \
       os.environ.get('LOCAL_PRODUCTION') == 'DISABLE_SECURITY':
        return True
    if username != os.environ.get('LOG_USERNAME'):
        return False
    if password != os.environ.get('LOG_PASSWORD'):
        return False
    return True


@app.route('/dev', methods=['GET', 'POST'])
@auth.login_required
def log_dev():
    add_to_log('dev')
    return ''


@app.route('/test', methods=['GET', 'POST'])
@auth.login_required
def log_test():
    add_to_log('dev')
    return ''


@app.route('/log', methods=['GET', 'POST'])
@auth.login_required
def log_prod():
    add_to_log('dev')
    return ''
