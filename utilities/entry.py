from datetime import datetime, date, timedelta
import os
import json
import urllib.parse
from urllib.parse import parse_qs
import base64
import boto3
from utilities.sftp_connection import (
    get_sftp_connection,
)
from utilities.slack_util import (
    send_slack_folder_1_found,
    send_slack_confirmed_job
)
from utilities.db import (
    add_folder_1_job,
    update_folder_1_job_timestamp,
    get_job,
    confirm_job,
)
def check_folder_1():
    new_files = []
    with get_sftp_connection() as sftp:
        for f in sftp.listdir_attr("Folder-Name"):
            #Check for files added in last hour
            file_dt = datetime.fromtimestamp(f.st_mtime)
            if( file_dt > (datetime.now() - timedelta(hours=1))):
                new_files.append({
                    'name':f.filename,
                    'date_added': file_dt.strftime("%m/%d/%Y, %H:%M")
                })

    if new_files:
        #Create dynamo object to get ID for button
        record_id = add_folder_1_job(new_files)
        #Send slack message and get corresponding timestamp to reply later
        slack_ts = send_slack_folder_1_found(new_files,record_id)
        #update dynamo object with the timestamp
        update_folder_1_job_timestamp(record_id,slack_ts)

    else:
        print("No new Files Found")

def handle_slack_response(event):
    #slack payload is x-www-form-urlencoded so we need to first base64 decode the lambda
    #event body and then decode the urlencoded payload
    b64_decoded = base64.b64decode(event['body']).decode("utf-8")
    url_decoded = urllib.parse.unquote_plus(b64_decoded)
    #Strip payload text and parse json
    url_decoded = url_decoded.replace("payload=", "")
    json_payload = json.loads(url_decoded)
    print(json_payload)
    action_id = json_payload['actions'][0]['value']

    #Get job from dynamo
    job = get_job(action_id)
    confirm_job(job['id'])
    send_slack_confirmed_job(job['slack_ts'])
    