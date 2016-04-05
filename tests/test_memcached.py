from sandpiper.util              import StandardTests
from sandpiper.adapter.memcached import Memcached, get_default_client

class FunctionalDefault(StandardTests):
    def get_driver(self):
        storage = get_default_client()

        return Memcached(storage)

class FunctionalCluster(StandardTests):
    def get_driver(self):
        storage = get_default_client([
            ('localhost', 11211),
            ('127.0.0.1', 11211),
        ])

        return Memcached(storage)

class FunctionalWithNamespace(StandardTests):
    def get_driver(self):
        storage = get_default_client()

        return Memcached(storage, 'ftest')
