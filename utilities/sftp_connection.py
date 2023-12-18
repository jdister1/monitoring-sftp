import paramiko
import io
import boto3
import base64
import json

def get_sftp_connection():
    client = boto3.client('secretsmanager')
    sftp_keys_raw = client.get_secret_value(
        SecretId="sftp-keys",
    )
    sftp_keys = json.loads(sftp_keys_raw['SecretString'])
    pem_file = client.get_secret_value(
        SecretId="sftp-pem",
    )
    with open('/tmp/sftp.pem', mode='w') as f:
        print(pem_file['SecretString'], file=f)
    
    host = sftp_keys['sftp_host']
    port = int(sftp_keys['sftp_port'])
    mykey = paramiko.RSAKey.from_private_key_file('/tmp/sftp.pem',password=sftp_keys['key_password'])
    transport = paramiko.Transport(host,port)
    transport.connect(username=sftp_keys['sftp_username'], pkey = mykey)

    return paramiko.SFTPClient.from_transport(transport)
