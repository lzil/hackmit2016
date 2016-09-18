import boto3

db_name = 'image-db'
primary_key = 'searchID'

def create_table():
    """
    create_table() creates a new table.
    """
    # connection manager
    dynamodb = boto3.resource('dynamodb',
            region_name='us-east-1',
            endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.create_table(
        TableName=db_name,
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    print("Table status:", table.table_status)

if __name__ == "__main__":
    create_table()
