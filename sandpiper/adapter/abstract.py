class Abstract(object):
    def get(self, key):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def remove(self, key):
        raise NotImplementedError()

    def find(self, pattern):
        raise NotImplementedError()
