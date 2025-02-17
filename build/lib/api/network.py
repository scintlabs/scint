from __future__ import annotations

from importlib import import_module
from collections import deque

import redis
import networkx as nx
import numpy as np
from meilisearch_python_sdk import AsyncClient as AsyncMeilisearch
from redis.asyncio import Redis as AsyncRedis

from scint.api.types import Trait, Struct
from scint.support.utils import env


class Providers(Struct):
    search = AsyncMeilisearch(env("MEILISEARCH_URL"), env("MEILISEARCH_API_KEY"))
    pubsub_redis = AsyncRedis.from_url(env("REDIS_URL"))
    queue_redis = redis.Redis(host=env("REDIS_URL"), port=6379, db=0)


class Resources(Struct): ...


class Catalog(Trait):
    def list_catalog(self):
        return {self.name: [item.name for item in self.items]}

    def catalog(self, name, module_paths):
        classes = self.get_module(module_paths)
        return dict(name, {c.name: c for c in classes})

    def get_module(self, module_paths):
        try:
            classes = []
            for path in module_paths:
                module = import_module(path)
                classes.extend(getattr(module, "__all__"))
            return classes
        except ImportError as e:
            print(f"Error: '{self.name}' not found. {str(e)}")
            return None


class Network:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_struct(self, struct: Struct):
        self.graph.add_node(struct.id, struct=struct)

    def connect(self, first: Struct, second: Struct, rel="linked", weight=1.0):
        self.graph.add_edge(first.id, second.id, relationship=rel, weight=weight)

    def accept(self, visitor):
        visitor.visit_network(self)
        visited = set()

        for node_id, data in self.graph.nodes(data=True):
            struct = data["struct"]
            struct.accept(visitor, visited)

        for from_id, to_id, edge_data in self.graph.edges(data=True):
            from_struct = self.graph.nodes[from_id]["struct"]
            to_struct = self.graph.nodes[to_id]["struct"]
            visitor.visit_edge(from_struct, to_struct, edge_data)

    def search_embeddings(self, struct: Struct, top_k=1):
        target_vec = self.graph.nodes[id(struct)]["embedding"]
        similarities = {}

        for node, data in self.graph.nodes(data=True):
            if node == id(struct):
                continue
            other_vec = data["embedding"]
            similarity = np.dot(target_vec, other_vec) / (
                np.linalg.norm(target_vec) * np.linalg.norm(other_vec)
            )
            similarities[node] = similarity

        closest_nodes = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[
            :top_k
        ]
        return [(self.graph.nodes[n]["struct"], score) for n, score in closest_nodes]

    def search_labels(self, struct: Struct, keyword):
        queue = deque([id(struct)])
        visited = set()
        results = []

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)

            struct_data = self.graph.nodes[node]
            if keyword in struct_data["keywords"]:
                results.append(struct_data["struct"])

            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)

        return results
