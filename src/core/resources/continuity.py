from __future__ import annotations

from datetime import timedelta
from typing import Any, Sequence, List, Type

from attrs import define
from meilisearch_python_sdk.models.search import Hybrid

from src.runtime.actor import Actor
from src.runtime.threads import Threads
from src.services.indexes import Indexes


THREAD_TIMEOUT = timedelta(minutes=30)
SIMILARITY_THRESHOLD = 0.85


def build(self, obj: Any):
    content = ""
    if isinstance(obj, Message):
        content += "\n\n".join(c for c in obj.content)
    elif isinstance(obj, Type):
        dct = self.serialize(obj)
        content += dct.get("content", "")
    elif isinstance(obj, List) and isinstance(all(obj), str):
        content += "\n\n".join(c for c in obj)
    elif isinstance(obj, List) and hasattr(all(obj), "content"):
        content += "\n\n".join(c.content for c in obj)
    elif isinstance(obj, str):
        content += obj
    return content


def _join(parts: Sequence[str]) -> str:
    return "\n\n".join(p for p in parts if p)


@define
class Continuity(Actor):
    _indexes: Indexes = Indexes()
    _threads: Threads = Threads()

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

    async def get_context(self, msg: Message):
        thread = await self.resolve_thread(msg)
        context = Context(
            active=ActiveContext(thread=thread),
            recent=RecentContext(threads=self.get_threads()),
            semantic=SemanticContext(embed=msg.metadata.embedding, search=self.search),
        )
        await context.update(msg)
        return context

    async def search(self, embed: List[float], top_k: int):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        q = Search(query="", hybrid=hybrid, vector=embed, limit=top_k)
        idx = await self._indexes.get_index("threads")
        res = idx.search(q)
        return SearchHits(hits=res.hits)
