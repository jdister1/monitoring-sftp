def add_folder_1_job(new_files):
    dynamodb = boto3.resource('dynamodb')
    dbtable = dynamodb.Table("my-sftp-watch")

    record_id = str(uuid.uuid4())
    
    #write to table
    dbtable.put_item(
        Item = {
            'id':  record_id,
            'files': json.dumps(new_files),
            'type': 'folder_1_files',
            'confirmed': False,
            'processed': False,
            'slack_ts': None,
            'date_added': datetime.now().strftime("%Y-%m-%d")
        }
    )

    return record_id

def update_folder_1_job_timestamp(record_id, slack_ts):
    dynamodb = boto3.resource('dynamodb')
    dbtable = dynamodb.Table("my-sftp-watch")

    response = dbtable.update_item(
        Key={
            'id':record_id
        },
        UpdateExpression = "set slack_ts=:val1",
        ExpressionAttributeValues = {
            ':val1': slack_ts
        },
        ReturnValues="UPDATED_NEW"
    )

def confirm_job(record_id):
    dynamodb = boto3.resource('dynamodb')
    dbtable = dynamodb.Table("my-sftp-watch")

    confirmed=True
    response = dbtable.update_item(
        Key={
            'id':record_id
        },
        UpdateExpression = "set confirmed=:val1",
        ExpressionAttributeValues = {
            ':val1': confirmed
        },
        ReturnValues="UPDATED_NEW"
    )