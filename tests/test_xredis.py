import os

from sandpiper.util           import StandardTests
from sandpiper.adapter.xredis import Adapter, create_client

class FunctionalDefault(StandardTests):
    def get_driver(self):
        storage = create_client(host = 'localhost', port = os.getenv('LXC_REDIS_PORT') or 6379)

        return Adapter(storage)

    def test_find(self):
        fixtures = [
            ('user:juti_noppornpitak', {'name': 'Juti Noppornpitak'}),
            ('user:kanata_iwata',      {'name': 'Kanata, Iwata'}),
            ('pass:clearance.1',       {'user': 'kanata_iwata'}),
        ]

        for k, v in fixtures:
            self.driver.set(k, v)

        found_keys   = self.driver.find('pass:clearance.*', only_keys=True)
        found_map    = self.driver.find('pass:clearance.*', only_keys=False)
        found_result = self.driver.find('user:*')

        self.assertEqual(['pass:clearance.1'], found_keys)
        self.assertEqual('kanata_iwata', found_map['pass:clearance.1']['user'])

class FunctionalWithNamespace(StandardTests):
    def get_driver(self):
        storage = create_client(host = 'localhost')

        return Adapter(storage, 'ftest')

    def test_find(self):
        fixtures = [
            ('user:juti_noppornpitak', {'name': 'Juti Noppornpitak'}),
            ('user:kanata_iwata',      {'name': 'Kanata, Iwata'}),
            ('pass:clearance.1',       {'user': 'kanata_iwata'}),
        ]

        for k, v in fixtures:
            self.driver.set(k, v)

        found_keys   = self.driver.find('pass:clearance.*', only_keys=True)
        found_map    = self.driver.find('pass:clearance.*', only_keys=False)
        found_result = self.driver.find('user:*')

        self.assertEqual(['pass:clearance.1'], found_keys)
        self.assertEqual('kanata_iwata', found_map['pass:clearance.1']['user'])
