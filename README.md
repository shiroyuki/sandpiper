# Sandpiper

A simple generic key-value store interface library.

## Requirements

* Python 3.4 or newer
* **boto3** for AWS DynamoDB (optional)
* **redis** for AWS DynamoDB (optional, future)
* **pymongo** for MongoDB (optional, future)

*Note: this may work with Python 2.7 but it will not be tested.*

## How to Install

Run `pip3 install sandpiper`.

## Example

```python
import boto3

from sandpiper         import Storage
from sandpiper.adapter import DynamoDB

ddb = boto3.resource(
    'dynamodb',
    endpoint_url='http://127.0.0.1:8000',
    region_name='us-east-1',
    aws_access_key_id='anything',
    aws_secret_access_key='anything',
    use_ssl=False,
    verify=False
)

driver = DynamoDB(ddb)

storage = Storage(driver)

# Set the data.
storage['user.1'] = {'name': 'foo'}
# Alternative: storage.set('user.1', {'name': 'foo'})

# Get the data.
print(storage['user.1']['name']) # -> foo
# Alternative: storage.get('user.1')

# Delete the data
del storage['user.1']
# Alternative: storage.remove('user.1')
```

## Currently Supported Storage Types

* In-memory/Python's built-in dictionary type (default)
* AWS DynamoDB

## Soon-to-be Supported Storage Types

* Redis
* MongoDB
