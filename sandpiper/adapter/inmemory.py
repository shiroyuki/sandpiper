from .abstract  import Abstract
from .exception import NotSupported

class InMemory(object):
    def __init__(self, storage=None):
        self._storage = storage or {}

    def get(self, key):
        if key not in self._storage:
            return None

        return self._storage[key]

    def set(self, key, value):
        self._storage[key] = value

    def remove(self, key):
        if key not in self._storage:
            return

        del self._storage[key]

    def find(self, *args, **kwargs):
        raise NotSupported()
