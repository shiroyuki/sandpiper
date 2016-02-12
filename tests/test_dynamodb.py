import boto3
import logging

from sandpiper.util             import StandardTests
from sandpiper.adapter.dynamodb import DynamoDB

logging.getLogger('boto3').setLevel(logging.CRITICAL)

class Unit(StandardTests):
    def get_driver(self):
        self.ddb = boto3.resource(
            'dynamodb',
            endpoint_url='http://127.0.0.1:8000',
            region_name='us-east-1',
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            use_ssl=False,
            verify=False
        )

        return DynamoDB(self.ddb)

    def ready_driver(self):
        self.driver.prepare()

    def kill_driver(self):
        self.driver._table().delete()
