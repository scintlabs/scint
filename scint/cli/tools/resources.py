from __future__ import annotations

from importlib import import_module

from meilisearch_python_sdk import AsyncClient as AsyncMeilisearch
import redis
from redis.asyncio import Redis as AsyncRedis

from scint.api.types import Trait, Struct
from scint.support.utils import env


class Resources(Struct):
    search = AsyncMeilisearch(env("MEILISEARCH_URL"), env("MEILISEARCH_API_KEY"))
    pubsub_redis = AsyncRedis.from_url(env("REDIS_URL"))
    queue_redis = redis.Redis(host=env("REDIS_URL"), port=6379, db=0)


class Catalog(Trait):
    def list_catalog(self):
        return {self.name: [item.name for item in self.items]}

    def create_factory(self, class_name: str, *args, **kwargs):
        def factory(obj, **arguments):
            return obj(**arguments)

        obj = self.factories.get(class_name)
        if obj:
            return factory(*args, **kwargs)
        else:
            raise ValueError(f"No factory found for {class_name}")

    def _build(self, name, module_paths):
        classes = self._import(module_paths)
        return dict(name, {c.name: c for c in classes})

    def _import(self, module_paths):
        try:
            classes = []
            for path in module_paths:
                module = import_module(path)
                classes.extend(getattr(module, "__all__"))
            return classes
        except ImportError as e:
            print(f"Error: '{self.name}' not found. {str(e)}")
            return None


app = {
    "domain": {
        "aspects": [
            {"name": "attention", "instances": []},
            {"name": "crawler", "instances": {}},
            {
                "name": "memory",
                "components": {
                    "event_source": {},
                    "indexes": [],
                    "context": {"map": {}},
                    "state": {"map": {}},
                },
            },
        ],
        "broadcast": {
            "channels": [],
            "routes": [],
            "bridges": [],
        },
        "resources": {
            "library": {
                "models": {},
                "prompts": {},
                "traits": {},
                "tools": {},
            },
            "parse": {
                "specifications": {},
            },
            "build": {
                "rules": {},
                "arguments": {},
                "factories": {},
            },
        },
        "structs": [
            {
                "id": "id",
                "parent": {},
                "siblings": {"left": {}, "right": {}},
                "children": [{}, {}, {}, {}],
                "traits": [
                    {"name": "function"},
                    {"name": "function"},
                    {"name": "function"},
                ],
                "state": {
                    "messages": [],
                    "tools": [],
                    "metadata": {
                        "labels": [],
                        "embeddings": [],
                    },
                },
            },
            {
                "id": "id",
                "parent": {},
                "siblings": {"left": {}, "right": {}},
                "children": [
                    {
                        "id": "id",
                        "parent": {},
                        "siblings": {"left": {}, "right": {}},
                        "children": [
                            {
                                "id": "id",
                                "parent": {},
                                "siblings": {"left": {}, "right": {}},
                                "children": [{}, {}, {}, {}],
                                "traits": [
                                    {"name": "function"},
                                    {"name": "function"},
                                    {"name": "function"},
                                ],
                                "state": {
                                    "aggregates": {
                                        "labels": [],
                                        "embeddings": [],
                                        "objects": [
                                            {"messages": []},
                                            {"tools": []},
                                        ],
                                    }
                                },
                            }
                        ],
                        "traits": [
                            {"name": "function"},
                            {"name": "function"},
                            {"name": "function"},
                        ],
                        "state": {
                            "aggregates": {
                                "labels": [],
                                "embeddings": [],
                                "objects": [
                                    {"messages": []},
                                    {"tools": []},
                                ],
                            }
                        },
                    },
                ],
                "traits": [
                    {"name": "function"},
                    {"name": "function"},
                    {"name": "function"},
                ],
                "state": {
                    "aggregates": {
                        "labels": [],
                        "embeddings": [],
                        "objects": [
                            {"messages": []},
                            {"tools": []},
                        ],
                    }
                },
            },
            {
                "id": "id",
                "parent": {},
                "siblings": {"left": {}, "right": {}},
                "children": [{}, {}, {}, {}],
                "traits": [
                    {"name": "function"},
                    {"name": "function"},
                    {"name": "function"},
                ],
                "state": {
                    "aggregates": {
                        "labels": [],
                        "embeddings": [],
                        "objects": [
                            {"messages": []},
                            {"tools": []},
                        ],
                    }
                },
            },
        ],
    },
}
