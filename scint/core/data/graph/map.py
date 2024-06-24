import datetime
from uuid import uuid4

import numpy as np

from scint.core.containers.blocks import Block
from scint.messaging.models import Message, SystemMessage
from scint.support.logging import log
from scint.core.graph.location import Location


class Map:
    def __init__(self):
        self.locations = {}

    def find_location(self, query, obj):
        pass

    def find_container(self):
        pass

    def find_context(self):
        pass

    def add_location(self, location):
        self.locations[location] = Location()

    def remove_location(self, location):
        pass

    def add_waypoint(self, location, other):
        pass

    def remove_waypoint(self, waypoint):
        pass
