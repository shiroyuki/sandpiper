from sandpiper.util           import StandardTests
from sandpiper.adapter.xredis import Adapter, create_client

class FunctionalDefault(StandardTests):
    def get_driver(self):
        storage = create_client(host = 'localhost')

        return Adapter(storage)

class FunctionalWithNamespace(StandardTests):
    def get_driver(self):
        storage = create_client(host = 'localhost')

        return Adapter(storage, 'ftest')
