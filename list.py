# list service

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
import decimal
import time
import datetime

# Check if connected to dynamodb

def check_connection(table_client):
    try:
        table_client.table_status
        return True
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False