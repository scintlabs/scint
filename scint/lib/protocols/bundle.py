from __future__ import annotations

from logging import Handler

from scint.lib.exchange import Publishable, Subscribable
from scint.lib.context import Context
from scint.lib.observability import Observable, Observant
from scint.lib.processor import Processor
from scint.lib.protocols import Channel
from scint.lib.struct import Struct
from scint.lib.traits import Trait, Traits


class Bundled(Trait):
    def broadcast(self, handler: Handler):
        pass

    def remove_member(self, handler: Handler):
        self.pool.remove(handler)

    def connect(self, other_node, interface_type="direct"):
        self.interfaces[other_node.node_id] = interface_type

    def share_context(self, other_node, key):
        if key in self.context.data:
            other_node.context.update(key, self.context.data[key])

    def disconnect(self, other_node):
        if other_node.node_id in self.interfaces:
            del self.interfaces[other_node.node_id]


class Bundle(Struct):
    context = Context()
    traits = Traits(Bundled, Observable, Observant, Publishable, Subscribable)
    processor = Processor()
    handlers = {}
    channels: Channel = {}
