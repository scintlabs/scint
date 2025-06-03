from __future__ import annotations

from typing import List, Type

from meilisearch_python_sdk.models.search import Hybrid
from monotonic import monotonic
from attrs import define, field
from datetime import timedelta

from src.base.actor import Actor
from src.base.utils import cosine_similarity, iso_to_epoch
from src.interpret.context import ActiveContext, Context, RecentContext
from src.interpret.threads import ActiveThread, Threads, Thread
from src.base.records import Message, Metadata, Search, SearchHits
from src.svc.indexes import Indexes


THREAD_TIMEOUT = timedelta(minutes=30)
SIMILARITY_THRESHOLD = 0.85


@define
class Continuity(Actor):
    indexes: Indexes = field(default=None)
    threads: Threads = Threads(
        None, None, 5, 10, 25, lambda stale: not stale.metadata.keywords
    )

    def get_threads(self, kind: Type[Thread] = None):
        return list(self.threads.walk(kind) if kind else self.threads.walk())

    async def resolve_thread(self, msg: Message) -> Thread:
        now = monotonic()
        best_thread = None
        best_drift = -1.0

        for t in self.threads.walk(ActiveThread):
            if not t.metadata.embedding:
                continue

            drift = cosine_similarity(msg.metadata.embedding, t.metadata.embedding)
            age = now - iso_to_epoch(t.metadata.events[-1]["created"]())

            if drift >= SIMILARITY_THRESHOLD and age <= THREAD_TIMEOUT:
                if drift > best_drift:
                    best_thread, best_drift = t, drift

        if best_thread is not None:
            return best_thread

        return await self._create_thread(msg)

    async def search(self, embed: List[float], top_k: int):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        q = Search(query="", hybrid=hybrid, vector=embed, limit=top_k)
        idx = await self.indexes.get_index("threads")
        res = idx.search(q)
        return SearchHits(hits=res.hits)

    async def _create_thread(self, msg: Message):
        metadata = Metadata(embedding=msg.metadata.embedding)
        thread = self.threads.append(metadata=metadata)
        await thread.update(msg)
        return thread

    async def get_context(self, msg: Message):
        thread = await self.resolve_thread(msg)
        context = Context(
            active=ActiveContext(thread), recent=RecentContext(self.get_threads())
        )
        await context.update(msg)
        return context
