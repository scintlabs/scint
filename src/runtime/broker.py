from __future__ import annotations

from typing import Any, List, Type

from attrs import define, field
from meilisearch_python_sdk.models.search import Hybrid

from src.base.actor import Actor
from src.base.records import Message
from src.base.metadata import Metadata
from src.continuity.context import Context
from src.continuity.threads import Thread, Threads
from src.resources.outlines import Outline
from src.resources.search import Search, SearchHits
from src.services.indexes import Indexes
from src.services.storage import Storage


@define(slots=True)
class Envelope:
    sender: str = field(default=None)
    content: Any = field(default=None)
    correlation: str = field(default=None)
    metadata: Metadata = field(default=None)

    @classmethod
    def create(cls, sender: str, payload: Any):
        return cls(sender=sender, payload=payload, metadata=Metadata())


@define
class Broker(Actor):
    _indexes: Indexes = field(default=None)
    _storage: Storage = field(default=None)
    _threads: Threads = field(default=None)

    def get_threads(self, kind: Type[Thread] = None):
        return list(self._threads.walk(kind) if kind else self._threads.walk())

    async def resolve_thread(self, msg: Message) -> Thread:
        if hasattr(msg, "metadata"):
            return await self.create_thread(msg)
        metadata = Metadata()
        thread = self._threads.append(metadata=metadata)
        await thread.update(msg)
        return thread

    async def create_thread(self, msg: Message):
        metadata = getattr(msg, "metadata", Metadata())
        thread = self._threads.append(metadata=metadata)
        await thread.update(msg)
        return thread

    async def search(self, embed: List[float], top_k: int):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        q = Search(query="", hybrid=hybrid, vector=embed, limit=top_k)
        idx = await self._indexes.get_index("threads")
        res = idx.search(q)
        return SearchHits(hits=res.hits)

    async def on_receive(self, env: Envelope):
        mdl = env.content
        if isinstance(mdl, Message):
            target = self._registry.get("interpreter")
        elif isinstance(mdl, Context):
            target = self._registry.get("composer")
        elif isinstance(mdl, Outline):
            target = self._registry.get("executor")
        else:
            target = None

        if target is None:
            raise RuntimeError("Dispatcher missing target for " f"{type(mdl).__name__}")
        target.tell(mdl, sender=self.address())
