import base64
from Crypto.Cipher import AES
import os
import re
import boto3
from datetime import datetime, timezone
from Crypto.Random import get_random_bytes
import binascii
from shutil import copyfile

log_file = '/opt/app/local_storage/log.txt'
encrypted_log_file = '/opt/app/local_storage/encrypted_log.txt'
max_log_size = os.environ.get('MAX_LOG_SIZE') or 1000000


def hex_str_to_bytes(hex_str_to_convert):
    byte_array = []
    for i in range(0, len(hex_str_to_convert), 2):
        byte_array.append(int(hex_str_to_convert[i:i + 2], 16))
    return bytes(byte_array)


def bytes_to_b64_str(bytes_to_convert):
    # return base64.b64encode(bytes_to_convert).decode('ascii')
    return base64.b64encode(bytes_to_convert).decode('utf-8')


def b64_str_to_bytes(str_to_convert):
    # return base64.b64decode(str_to_convert.encode('ascii'))
    str_to_convert = str_to_convert
    return base64.b64decode(str_to_convert.encode('utf-8'))


def get_aes_key():
    return os.environ.get('LOG_AES_KEY') or \
        '7ec330898064b7e5f267602b64aa25a3a1c09b3c7fa4309e4712859c00ffe588'


def get_aes_key_bytes():
    return hex_str_to_bytes(get_aes_key())


def generate_aes_key():
    key = get_random_bytes(32)
    key_hex_string = binascii.hexlify(key).decode('ascii')
    return key_hex_string


def encrypt(plain_text, key=get_aes_key_bytes(),
            min_length_for_padding=0, padding_char=' '):
    # Convert key to bytes type if not already
    key_bytes = key
    if type(key) == str:
        key_bytes = hex_str_to_bytes(key)
    cipher = AES.new(key_bytes, AES.MODE_EAX)
    nonce = cipher.nonce
    padded = plain_text + ' ' * (min_length_for_padding - len(plain_text))
    ciphertext, tag = cipher.encrypt_and_digest(padded.encode('utf-8'))
    encypted_payload = tag + nonce + ciphertext
    return bytes_to_b64_str(encypted_payload)


# Decrypt either string or file
def decrypt(encrypted_str_or_file, key=get_aes_key_bytes(), padding_char=' '):
    encrypted_str = encrypted_str_or_file
    if os.path.isfile(encrypted_str_or_file):
        with open(encrypted_str_or_file, 'r') as f:
            encrypted_str = f.read()

    # Convert key to bytes type if not already
    key_bytes = key
    if type(key) == str:
        key_bytes = hex_str_to_bytes(key)
    encrypted_bytes = b64_str_to_bytes(encrypted_str)
    tag = encrypted_bytes[0:16]
    nonce = encrypted_bytes[16:32]
    ciphertext = encrypted_bytes[32:]
    cipher = AES.new(key_bytes, AES.MODE_EAX, nonce=nonce)
    plain_text = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    return plain_text.rstrip(padding_char)


def upload_file(bucket, file_path, file_name):
    log_storage_address = os.environ.get('LOG_STORAGE_ADDRESS') or 'local'

    if log_storage_address == 'local':
        local_path = f'./local_storage/{bucket}'
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        copyfile(encrypted_log_file, f'{local_path}/{file_name}')
        return

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
    client.upload_file(encrypted_log_file, bucket, file_name)


def encrypt_file():
    encrypted = ''
    with open(log_file, 'r') as f:
        contents = f.read()
        encrypted = encrypt(contents)
    with open(encrypted_log_file, 'w') as f:
        f.write(encrypted)


def write_to_storage(path):
    now = datetime.now(timezone.utc)
    dt_string = now.strftime("%Y.%m.%d-%H.%M.%S.%f")
    file_name = f'{dt_string}.txt'
    upload_file(path, '/opt/app', file_name)


def add_to_log(path, data):
    with open(log_file, 'a+') as f:
        f.write(data)
    print(os.path.getsize(log_file), max_log_size)
    if os.path.isfile(log_file) and os.path.getsize(log_file) > int(max_log_size):
        encrypt_file()
        os.remove(log_file)
        write_to_storage(path)
        os.remove(encrypted_log_file)
