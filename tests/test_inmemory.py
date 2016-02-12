from sandpiper.util             import StandardTests
from sandpiper.adapter.inmemory import InMemory

class Unit(StandardTests):
    def get_driver(self):
        return InMemory()
