# from __future__ import annotations

# from typing import Any, Dict, List, Optional
# from typing_extensions import Callable, TypeVar, ParamSpec

# import redis
# from meilisearch_python_sdk import AsyncClient as AsyncMeilisearch
# from redis.asyncio import Redis as AsyncRedis

# from scint.framework.support.models import Model


# T = TypeVar("T")
# P = ParamSpec("P")


# class Parameter(Model):
#     type: str
#     name: str
#     description: str
#     value: Optional[List[Any]] = None

#     @property
#     def model(self):
#         prop = {"type": self.type, "description": self.description}
#         if self.type == "enum":
#             prop["enum"] = self.items
#         elif self.type == "array":
#             prop["array"] = self.items

#         return prop


# class Parameters(Model):
#     parameters: List[Parameter]

#     @property
#     def model(self):
#         return {
#             "type": "object",
#             "properties": {p.name: {**p.model} for p in self.parameters},
#             "required": [p.name for p in self.parameters],
#             "additionalProperties": False,
#         }


# class Channel(Model):
#     name: str
#     description: str
#     members: Dict[str, Dict[Any, Callable]]


# class Process(Model):
#     intention: List[Intention] = []
#     tasks: List[Task] = []
#     tools: List[Tool] = []


# class Messages(Model):
#     prompts: List[Prompt] = []
#     messages: List[Message] = []
#     responses: List[Response] = []


# class Context(Model):
#     messages: Messages
#     process: Process


# class Providers(Struct):
#     search = AsyncMeilisearch(env("MEILISEARCH_URL"), env("MEILISEARCH_API_KEY"))
#     pubsub_redis = AsyncRedis.from_url(env("REDIS_URL"))
#     queue_redis = redis.Redis(host=env("REDIS_URL"), port=6379, db=0)


# app = {
#     "aspects": [
#         {"name": "attention", "instances": []},
#         {"name": "crawler", "instances": {}},
#         {
#             "name": "memory",
#             "components": {
#                 "event_source": {},
#                 "indexes": [],
#                 "context": {"map": {}},
#                 "state": {"map": {}},
#             },
#         },
#     ]
# }

# channels = {
#     "channels": [],
#     "routes": [],
#     "bridges": [],
# }

# resources = {
#     "catalog": {
#         "models": {},
#         "prompts": {},
#         "traits": {},
#         "tools": {},
#     },
#     "build": {
#         "rules": {},
#         "arguments": {},
#         "factories": {},
#     },
# }

# network = [
#     {
#         "id": "id",
#         "data": {
#             "messages": [],
#             "tools": [],
#             "metadata": {
#                 "labels": [],
#                 "embeddings": [],
#             },
#         },
#         "traits": [],
#         "origin": {},
#         "children": [{}, {}, {}, {}],
#     }
# ]
