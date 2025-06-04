from __future__ import annotations

from typing import Any, Sequence, List, Type

from attrs import define
from meilisearch_python_sdk.models.search import Hybrid
from monotonic import monotonic
from datetime import timedelta

from src.model.threads import Threads, Thread, ActiveThread
from src.model.context import Context, ActiveContext, RecentContext, SemanticContext
from src.model.records import Message, Metadata, Search, SearchHits
from src.runtime.actor import Actor
from src.runtime.utils import cosine_similarity, iso_to_epoch
from src.services.indexes import Indexes


THREAD_TIMEOUT = timedelta(minutes=30)
SIMILARITY_THRESHOLD = 0.85


@define
class Continuity(Actor):
    _threads: Threads = Threads()
    _indexes: Indexes = Indexes()

    def get_threads(self, kind: Type[Thread] = None):
        return list(self._threads.walk(kind) if kind else self._threads.walk())

    async def resolve_thread(self, msg: Message) -> Thread:
        now = monotonic()
        best_thread = None
        best_drift = -1.0

        for thread in self._threads.walk(ActiveThread):
            if not thread.metadata.embedding:
                continue

            drift = cosine_similarity(msg.metadata.embedding, thread.metadata.embedding)
            age = now - iso_to_epoch(thread.metadata.events[-1]["created"]())

            if drift >= SIMILARITY_THRESHOLD and age <= THREAD_TIMEOUT:
                if drift > best_drift:
                    best_thread, best_drift = thread, drift

        if best_thread is not None:
            return best_thread

        return await self.create_thread(msg)

    async def search(self, embed: List[float], top_k: int):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        q = Search(query="", hybrid=hybrid, vector=embed, limit=top_k)
        idx = await self._indexes.get_index("threads")
        res = idx.search(q)
        return SearchHits(hits=res.hits)

    async def create_thread(self, msg: Message):
        metadata = Metadata(embedding=msg.metadata.embedding)
        thread = self._threads.append(metadata=metadata)
        await thread.update(msg)
        return thread

    async def get_context(self, msg: Message):
        thread = await self.resolve_thread(msg)
        context = Context(
            active=ActiveContext(thread),
            recent=RecentContext(self.get_threads()),
            semantic=SemanticContext(embed=msg.metadata.embedding, search=self.search),
        )
        await context.update(msg)
        return context


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
