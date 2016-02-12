import boto3

# For a Boto3 client.
ddb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-east-1',
    aws_access_key_id='anything',
    aws_secret_access_key='anything'
)

response = ddb.create_table(
    TableName = 'dummy',
    KeySchema = [
        {
            'AttributeName': 'key',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions = [
        {
            'AttributeName': 'key',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput = {
        'ReadCapacityUnits':  5,
        'WriteCapacityUnits': 5,
    }
)
print(response)
#
# # For a Boto3 service resource
# ddb = boto3.resource('dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='us-west-1',
#     aws_access_key_id='anything',
#     aws_secret_access_key='anything'
# )
#
# print(list(ddb.tables.all()))
