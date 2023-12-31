# connect to dynamodb database using local dynamodb

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# create boto3 session
session = boto3.Session(profile_name='default')

# Connect to dynamodb
dynamodb = session.resource('dynamodb', region_name='ap-southeast-2', endpoint_url="http://localhost:8000")


# Create table if not exists
def create_table():
    try:
        table = dynamodb.create_table(
            TableName='todo_list',
            KeySchema=[
                {
                    'AttributeName': 'list_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'item_order',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'list_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'item_order',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='todo_list')

        # Print out some data about the table.
        print(table.item_count)
    except ClientError as e:
        print(e.response['Error']['Message'])

def connect_table():
    # connect to the table
    table = dynamodb.Table('todo_list')
    return table

def return_top_5(table = connect_table()):
    # return the top 5 items in the list
    response = table.query(
        KeyConditionExpression=Key('list_id').eq('1')
    )
    return response['Items']

def add_record(db_client, data):
    # add a record to the table

    db_client.put_item(
        TableName='todo_list',
        Item={
            'list_id': '1',
            'item_id': data['id'],
            'item_data': data['text'],
            'item_order': int(data['id'].split('-')[1])
        }
    )

    return
