# Sandpiper

A simple generic key-value store interface library.

## Requirements

* Python 3.4 or newer
* **boto3** for AWS DynamoDB (optional)
* **pymemcache** for Memcached (optional)
* **redis** for Redis (optional, future)
* **pymongo** for MongoDB (optional, future)

*Note: this may work with Python 2.7 but it will not be tested.*

## How to Install

Run `pip3 install sandpiper`.

## Example

### Set up the driver

First of all, let's set up the adapter.

#### For DynamoDB

```python
import boto3

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
```

#### For Memcached

```python
from sandpiper.adapter.memcached import Memcached, get_default_client

connection_list = [
    ('c1.shiroyuki.com', 11211),
    ('c2.shiroyuki.com', 11211),
    # ...
]

client = get_default_client(connection_list)
driver = Memcached(client, namespace = 'default', delimiter = ':')
```

### How to use it

```python
from sandpiper import Storage

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
* Memcached

## Soon-to-be Supported Storage Types

* Redis
* MongoDB
