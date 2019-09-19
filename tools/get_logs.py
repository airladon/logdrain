#
# get_logs PREFIX latest     download and decrypt the latest file in PREFIX
# get_logs PREFIX list       list all files with PREFIX
# get_logs latest            download and decrypt the latest file
# get_logs list              list all files
# get_logs FILE_NAME         download and decrypt a specific file
# get_logs PREFIX/           download all files with prefix
#
# Where PREFIX would be dev or prod or any other root folder in the remote
# storage

import os
import boto3
import re
from pathlib import Path
import sys
sys.path.insert(0, './app/app')
from tools import decrypt    # noqa

log_storage_address = os.environ.get('LOG_STORAGE_ADDRESS') or 'local'
region = re.search(
    r'\.([^\.]*)\.digitaloceanspaces.com$',
    log_storage_address).groups()[0]
bucket = re.search(
    r'https:\/\/([^\.]*)\.',
    log_storage_address).groups()[0]
log_storage_access_key = os.environ.get('LOG_STORAGE_ACCESS_KEY')
log_storage_secret = os.environ.get('LOG_STORAGE_SECRET_ACCESS_KEY')
session = boto3.session.Session()
client = session.client(
    's3',
    region_name=region,
    endpoint_url=f'https://{region}.digitaloceanspaces.com',  # noqa
    aws_access_key_id=log_storage_access_key,
    aws_secret_access_key=log_storage_secret,
)


def get_latest_file(prefix):
    prefix = prefix.strip('/')
    if len(prefix) > 1:
        prefix = prefix + '/'
    files = client.list_objects(Bucket=bucket, Prefix=prefix)['Contents']
    times = [file['LastModified'] for file in files if file['Key'][-1] != '/']
    latest_file = files[times.index(max(times))]
    local_file_name = f'./local_storage/{latest_file["Key"].split("/")[-1]}'
    client.download_file(bucket, latest_file['Key'], local_file_name)
    print('1 file downloaded')
    return latest_file['Key'], local_file_name


def get_file(file_name):
    local_file_name = f'./local_storage/{file_name.split("/")[-1]}'
    client.download_file(bucket, file_name, local_file_name)
    print('1 file downloaded')
    return file_name, local_file_name


def get_files(prefix):
    prefix = prefix.strip('/')
    files = client.list_objects(Bucket=bucket, Prefix=prefix)['Contents']
    files = [file for file in files if file['Key'][-1] != '/']
    for file in files:
        print(file['Key'])
        path = Path(f'./local_storage/{file["Key"]}')
        path.parent.mkdir(parents=True, exist_ok=True)
        local_file_name = f'./local_storage/{file["Key"]}'
        client.download_file(bucket, file['Key'], local_file_name)
    print(f'{len(files)} files downloaded')


def list_files(prefix):
    prefix = prefix.strip('/')
    if len(prefix) > 1:
        prefix = prefix + '/'
    files = client.list_objects(Bucket=bucket, Prefix=prefix)['Contents']
    files = [file for file in files if file['Key'][-1] != '/']
    for file in files:
        print(file['Key'])
    print(f'{len(files)} files listed')


get = ''
prefix = ''

if len(sys.argv) == 3:
    prefix = sys.argv[1]
    get = sys.argv[2]

if len(sys.argv) == 2:
    get = sys.argv[1]

if get == 'latest':
    remote_file_name, local_file_name = get_latest_file(prefix)
    print(f'{remote_file_name}:')
    print(decrypt(local_file_name))
    exit()

if get == 'list':
    list_files(prefix)
    exit()

if get[-1] == '/':
    get_files(prefix)
    exit()

remote_file_name, local_file_name = get_file(get)
print(f'{remote_file_name}:')
print(decrypt(local_file_name))
