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

## Currently Supported Storage Types

* In-memory/Python's built-in dictionary type (default)
* AWS DynamoDB

## Soon-to-be Supported Storage Types

* Redis
* MongoDB
