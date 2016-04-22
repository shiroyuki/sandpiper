import json

try:
    import redis
except ImportError as e:
    raise ImportError('Failed to import "redis" ({})'.format(e))

from .abstract import Abstract
from .abstract import NotSupported

import logging

def create_client(**pool_args):
    if 'port' not in pool_args:
        pool_args['port'] = 6379

    if 'host' not in pool_args:
        raise ValueError('"host" is not defined.')

    pool = redis.ConnectionPool(**pool_args)

    return redis.Redis(connection_pool=pool)

class Adapter(Abstract):
    def __init__(self, storage = None, namespace = None, delimiter = ':', auto_json_convertion = True):
        self._storage   = storage
        self._namespace = namespace or ''
        self._delimiter = delimiter

        self._auto_json_convertion = auto_json_convertion

    def get(self, key):
        actual_key = self._actual_key(key)
        value      = self._storage.get(actual_key)

        if not value:
            return value

        if self._auto_json_convertion:
            return json.loads(value.decode('utf-8'))

        return value

    def set(self, key, value):
        actual_key = self._actual_key(key)
        encoded    = value

        if self._auto_json_convertion:
            encoded = json.dumps(value)

        self._storage.set(actual_key, encoded)

    def remove(self, key):
        actual_key = self._actual_key(key)

        self._storage.delete(actual_key)

    def find(self, pattern='*', only_keys=False):
        actual_pattern = self._actual_key(pattern)
        if only_keys:
            return [
                key.decode('utf-8')
                for key in self._storage.keys(actual_pattern)
            ]

        return {
            key.decode('utf-8'): self.get(key)
            for key in self._storage.keys(actual_pattern)
        }

    def _actual_key(self, key):
        if not self._namespace:
            return key

        return '{}{}{}'.format(self._namespace, self._delimiter, key)
