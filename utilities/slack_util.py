import requests
import json
import boto3
from slack_sdk import WebClient

def get_slack_api_creds():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='my-slackbot-credentials',
    )
    return json.loads(response['SecretString'])
    
def send_slack_folder_1_found(file_names, job_id):
    client = WebClient(token=get_slack_api_creds()['bot_token'])
    result = client.chat_postMessage(
        channel=get_slack_api_creds()['channel_id'], 
        blocks=get_file_found_blocks(file_names, job_id,"new_files")
    )
    return result['ts']


def get_file_found_blocks(file_names, job_id, job_type):
    #Build out file name string   
    file_name_element_array = []
    file_name_elements = []
    file_name_element_array.append(
        
            {
                "type": "rich_text_section",
                "elements": [
                    {
                        "type": "text",
                        "text": "The following new files were uploaded to SFTP \n"
                    }
                ]
            }
        
    )
    
    for fn in file_names:
        file_name_elements.append(
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": fn['name'] + '   '
                        },
                        {
                            "type": "text",
                            "text": "(" + fn['date_added'] + ")",
                            "style": {
								"italic": True
							}
                        }
                    ]
                }
        )
    file_name_element_array.append(
            {
                "type": "rich_text_list",
                "style": "bullet",
                "elements": file_name_elements
            }
    )
    
    data = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Files Found",
                    "emoji": True
                }
            },
            {
                "type": "rich_text",
                "elements": file_name_element_array
            },  
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Confirm Files",
                            "emoji": True
                        },
                        "value": job_id,
                        "action_id": "process" + job_type
                    }
                ]
            }
        ]
    
    return data
    

def send_slack_confirmed_job(slack_ts):
    client = WebClient(token=get_slack_api_creds()['bot_token'])
    result = client.chat_postMessage(
        channel=get_slack_api_creds()['channel_id'], 
        text="This job was confirmed",
        thread_ts=slack_ts,
    )
    