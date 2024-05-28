from uuid import uuid4
import time
import asyncio
from collections import defaultdict

from scint.modules.storage import storage_controller
from scint.core.containers import Messages
from scint.modules.logging import log


class NodeType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        def metadata(self):
            return {
                "id": self.dsid,
                "name": self.name,
                "prompts": self.prompts.metadata,
                "messages": self.messages.metadata,
                "functions": self.functions.metadata,
            }

        def compose(self):
            comp = {}
            for key, value in self.__dict__.items():
                comp[key] = value
            return comp

        dct["dsid"] = str(uuid4())
        dct["name"] = name
        dct["description"] = None
        dct["compose"] = compose
        dct["metadata"] = property(metadata)
        dct["storage"] = storage_controller
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)


class Tree(metaclass=NodeType):
    def __init__(self):
        self.branches = []

    def add(self, child):
        self.branches.append(child)

    def remove(self, child):
        self.branches.remove(child)


class Graph(metaclass=NodeType):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = {}

    def add_node(self, node):
        log.info(f"Adding {node.name} to {self.origin.name} graph.")
        self.nodes.append(node)
        self.edges[node] = {}

    def add_edge(self, from_node, to_node, weight=1):
        log.info(f"Adding edge from {from_node} to {to_node} with weight {weight}")
        if from_node not in self.edges:
            self.edges[from_node] = {}
        self.edges[from_node][to_node] = weight
        if to_node not in self.edges:
            self.edges[to_node] = {}
        self.edges[to_node][from_node] = weight


class ContextGraph(metaclass=NodeType):
    def __init__(self, controller):
        self.controller = controller
        self.nodes = {}
        self.edges = defaultdict(dict)
        self.expiration_times = {}

    def add_context(self, node, parent=None):
        log.info(f"Adding {node.name} to the graph.")
        self.nodes[node.id] = node
        if parent:
            self.edges[parent.id][node.id] = 1
            self.edges[node.id][parent.id] = 1
        self.expiration_times[node.id] = time.time() + node.lifetime

    def add_link(self, from_node, to_node, weight=1):
        log.info(f"Adding edge from {from_node.id} to {to_node.id}.")
        self.edges[from_node.id][to_node.id] = weight
        self.edges[to_node.id][from_node.id] = weight

    def dismiss_context(self, node):
        log.info(f"Dismissing {node.id}.")
        del self.nodes[node.id]
        del self.expiration_times[node.id]
        for neighbor in self.edges[node.id]:
            del self.edges[neighbor][node.id]
        del self.edges[node.id]

    async def manage_lifecycles(self):
        while True:
            current_time = time.time()
            to_remove = [
                cid
                for cid, exp_time in self.expiration_times.items()
                if exp_time <= current_time
            ]
            for cid in to_remove:
                self.dismiss_context(self.nodes[cid])
            await asyncio.sleep(60)


class Thread(metaclass=NodeType):
    def __init__(self):
        super().__init__()
        self.name = "New Orphan Thread"
        self.description = "Anonymous orphan thread."
        self.messages = Messages(self)
        self.children = []
        self.prev = None
        self.next = None

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
