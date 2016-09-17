import boto3


dynamodb = boto3.resource('dynamodb',
        region_name='us-east-1',
        endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
        aws_secret_access_key="hI37+gaZ7+Sbpd1LxjfuY2INRquMX7AXQP/arFH8",
        aws_access_key_id="AKIAJNLHPPFJ2AJ7ZCOQ")

table = dynamodb.create_table(
    TableName='image-db',
    KeySchema=[
        {
            'AttributeName': 'search',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'title',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'search',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print("Table status:", table.table_status)