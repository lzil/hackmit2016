import boto3
import json
import decimal
import setup

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

db_name = 'image-db'
primary_key = 'searchID'

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# connection manager
dynamodb = boto3.resource('dynamodb',
        region_name='us-east-1',
        endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
        aws_secret_access_key="hI37+gaZ7+Sbpd1LxjfuY2INRquMX7AXQP/arFH8",
        aws_access_key_id="AKIAJNLHPPFJ2AJ7ZCOQ")

table = dynamodb.Table(db_name)

def insert(searchID, item):
    """
    insert(searchID, item) inserts a new item, given its searchID.
    The database response is returned.

    Params
        searchID is a string containing the query
        item is a dictionary of the new item
    """
    response = table.put_item(Item = item)
    nice_response = json.dumps(response, indent=4, cls=DecimalEncoder)

    return nice_response

def get(searchID):
    """
    get(searchID) searches for an item, given its searchID. If
    there is an error, there will be no return. The json item
    is returned.
    """
    try:
        response = table.get_item(Key={primary_key : year})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        nice_item = json.dumps(item, indent=4, cls=DecimalEncoder)
        print("GetItem succeeded:")
        print(nice_item)

        return nice_item

def delete(searchID):
    """
    delete(searchID) deletes an item, given its searchID.
    """
    try:
        response = table.delete_item(
            Key={
                primary_key: searchID
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        nice_response = json.dumps(response, indent=4, cls=DecimalEncoder)

        print("DeleteItem succeeded:")
        print(nice_response)

        return nice_response

