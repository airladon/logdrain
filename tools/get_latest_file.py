import os
import boto3
import re
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
    files = client.list_objects(Bucket=bucket, Prefix=f'{prefix}/')['Contents']
    times = [file['LastModified'] for file in files if file['Key'][-1] != '/']
    latest_file = files[times.index(max(times))]
    local_file_name = f'./local_storage/{latest_file["Key"].split("/")[-1]}'
    client.download_file(bucket, latest_file['Key'], local_file_name)
    return local_file_name


# def get_file(file_name):



file_name = get_latest_file(sys.argv[1])
print(decrypt(file_name))
