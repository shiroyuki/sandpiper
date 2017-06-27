import os
import threading
import time

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

    def test_concurrency(self):
        async_test_worker_count = 128

        async_test_workers = []
        failed_assertions  = []

        def test_read(key):
            time.sleep(0.2)

            try:
                assert self.driver.get(key)
            except AssertionError:
                failed_assertions.append(label)

        def test_write(key, data):
            time.sleep(0.2)

            self.driver.set(key, data)

        self.driver.set('sandpiper_test_key', 'foo')

        for iteration_index in range(async_test_worker_count):
            key   = 'sandpiper_test_key'
            value = 'sandpiper_test_value_{}'.format(iteration_index)

            async_test_workers.append(threading.Thread(daemon = True, target = test_write, args = (key, value)))
            async_test_workers.append(threading.Thread(daemon = True, target = test_read,  args = (key,)))

        for worker in async_test_workers:
            worker.start()

        for worker in async_test_workers:
            if worker.isAlive():
                worker.join()

        self.assertEqual(0, len(failed_assertions), ', '.join(failed_assertions))
