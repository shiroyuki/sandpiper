from sandpiper.util           import StandardTests
from sandpiper.adapter.xredis import Adapter, create_client

class FunctionalDefault(StandardTests):
    def get_driver(self):
        storage = create_client(host = 'localhost')

        return Adapter(storage)

    def test_find(self):
        fixtures = [
            ('user:juti_noppornpitak', {'name': 'Juti Noppornpitak'}),
            ('user:kanata_iwata',      {'name': 'Kanata, Iwata'}),
            ('pass:clearance.1',       {'user': 'kanata_iwata'}),
        ]

        for k, v in fixtures:
            self.driver.set(k, v)

        found_keys   = list(self.driver.find('pass:clearance.*', only_keys=True))
        found_result = dict(self.driver.find('user:*'))

        self.assertEqual(['pass:clearance.1'], found_keys)

class FunctionalWithNamespace(StandardTests):
    def get_driver(self):
        storage = create_client(host = 'localhost')

        return Adapter(storage, 'ftest')
