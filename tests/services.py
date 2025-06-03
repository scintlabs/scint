from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import Callable, Coroutine, Dict, Any, Union

from attrs import define, field


ServiceCallable = Callable[..., Union[Coroutine[Any, Any, Any], Any]]


_MODULES = ("src.lib.tools", "src.lib.instructions")


@define
class Services:
    _services: Dict[str, Dict[str, Any]] = field(factory=dict)

    def register(self, func: ServiceCallable):
        if func.__name__ in self._services:
            raise RuntimeError(f"Service '{func.__name__}' already registered")
        self._services[func.__name__] = {
            "worker": None,
            "task": None,
            "status": "stopped",
        }
        return func

    async def start(self, name: str, *args, **kwargs):
        service = self._services.get(name)
        if not service:
            raise KeyError(f"Unknown service '{name}'")
        if service["status"] == "running":
            return
        service["task"] = asyncio.create_task(service["worker"](), name=name)
        service["status"] = "running"

    async def stop(self, name: str):
        service = self._services.get(name)
        if not service or service["status"] != "running":
            return
        task: asyncio.Task = service["task"]
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        service["status"] = "stopped"
        service["task"] = None

    async def _shutdown(self, loop: asyncio.AbstractEventLoop, *_):
        print("\nShutting down …")
        for k in self._services.keys():
            await self.stop(k)
        loop.stop()


# async def sync(self, indexes: Indexes, library: Library):
#     indexed_ids = await self.index.indexed_ids()
#     current_ids = {t.id for t in self.registry.all()}
#     await self.index.purge(indexed_ids - current_ids)


# async def search(self, query: str, limit: int = 10):
#     await self.load()
#     sq = Search(
#         query=query,
#         limit=limit,
#         hybrid=Hybrid(semantic_ratio=0.9, embedder="default"),
#     )
#     return await self.index.search(sq)


# def save_tools(data: Dict[str, Any]):
#     with open(CONFIG_LIB, "w") as f:
#         f.write(json.dumps(data))
