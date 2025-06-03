# from __future__ import annotations

# import hashlib
# from importlib import import_module
# import inspect
# from typing import Any, Callable, Dict, TypeAlias, Union

# from attr import define
# from attrs import field
# from meilisearch_python_sdk.models.search import Hybrid, SearchResults

# from src.base.records import Search
# from src.svc.datastores import DataStore
# from src.svc.indexes import IndexProvider


# @define
# class Repository:
#     indexes: IndexProvider = IndexProvider()
#     tools: Dict[str, Any] = field(factory=load_tools)
#     stores: Dict[str, DataStore] = field(factory=dict)
#     registry: Dict[str, Callable] = field(factory=dict)

#     async def load(self):
#         if self._loaded:
#             return
#         async with self._lock:
#             if not self._loaded:
#                 await self._load_modules()
#                 self._loaded = True

#     async def search_tools(self, query: str, limit: int = 10):
#         await self.load()
#         sq = Search(
#             query=query,
#             limit=limit,
#             hybrid=Hybrid(semantic_ratio=0.9, embedder="default"),
#         )
#         return await self.index.search(sq)

#     async def execute_tool(self, name: str, args: Dict[str, Any]):
#         fn = self.registry.get(name)
#         if fn is None:
#             raise KeyError(f"Tool {name!r} not registered")
#         return await fn(**args)

#     async def _load_modules(self):
#         module = import_module("src.lib.tools")

#         for _, attr in inspect.getmembers(module):
#             if inspect.isfunction(attr) and attr.__module__ == module.__name__:
#                 fp = generate_signature(attr)
#                 wrapper = tool(attr)
#                 self.tools.setdefault("functions", {})[fp] = wrapper.schema
#                 await self._register_wrappers(wrapper)
#         await self._sync_index()

#     async def _register_wrappers(self, wrapper: Callable):
#         self.registry[wrapper.schema["name"]] = wrapper
#         record = {
#             "id": hashlib.sha1(wrapper.schema["name"].encode()).hexdigest(),
#             **wrapper.schema,
#         }
#         await self.index.add_records([record])

#     async def _sync_index(self):
#         hits: SearchResults = await self.index.search(Search("", limit=1000))
#         indexed_ids = {h["id"] for h in hits.hits}
#         current_ids = {
#             hashlib.sha1(name.encode()).hexdigest() for name in self.registry
#         }
#         stale = indexed_ids - current_ids
#         if stale:
#             await self.index.delete_records(list(stale))
#         save_tools(self.tools)


# REPOSITORY = Repository()
