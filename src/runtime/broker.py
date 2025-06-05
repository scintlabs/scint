from __future__ import annotations

from typing import Any, Dict, List, Type

from attrs import define, field
from meilisearch_python_sdk.models.search import Hybrid

from src.base.actor import Actor, Address
from src.base.records import Message, Outline
from src.base.metadata import Metadata
from src.continuity.context import Context
from src.continuity.threads import Thread, Threads
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
    _directory: Dict[str, Address] = field(factory=dict)

    async def on_receive(self, env: Envelope):
        content = env.content
        if isinstance(content, Message):
            dest = self._registry.get("interpreter")
        elif isinstance(content, Context):
            dest = self._registry.get("composer")
        elif isinstance(content, Outline):
            dest = self._registry.get("executor")
        else:
            dest = None

        if dest is None:
            raise RuntimeError(f"Unable to route {type(content).__name__}")

        dest.tell(content, sender=self.address())

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
