# connect to dynamodb database using local dynamodb

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
import decimal
import time
import datetime

# Connect to dynamodb
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', endpoint_url="http://localhost:8000")

# Create table if not exists
def create_table():
    try:
        # create dynamodb table
        # fields:
        # list_id: string
        # item_id: string
        # item_data: string
        # item_order: number
        # primary key: list_id
        # sort key: item_order

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

def add_record(dynamodb, data):
    # add a record to the table
    
    # data is shaped like this: {'id': 'item-1', 'text': 'New Item'}
    # id is the item_id, text is the item_data
    # id is the item_order, text is the item_data
    # list_id = 'todo_list'
    # dynamodb = dynamodb connection

    dynamodb.put_item(
        TableName='todo_list',
        Item={
            'list_id': '1',
            'item_id': data['id'],
            'item_data': data['text'],
            'item_order': int(data['id'].split('-')[1])
        }
    )

    return

return_top_5()