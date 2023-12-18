import json
import boto3
from datetime import datetime
import os
from utilities.entry import (
    check_folder_1,
    check_folder_2,
    check_folder_3,
    handle_slack_response
)

def lambda_handler(event, context):
    http_path = event["requestContext"]['http']['path']
    if http_path == "":
        print("ROOT")
    if http_path == "/slack-response":
        handle_slack_response(event)
    if http_path == "/check-folder-1":
        check_folder_1()
    if http_path == "/check-folder-2":
        check_folder_2()
    if http_path == "/check-folder-3":
        check_folder_3()

    return {
        'statusCode': 200,
        'body': json.dumps('Function Finished')
    }