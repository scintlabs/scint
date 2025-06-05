from __future__ import annotations

from functools import singledispatchmethod
from typing import List, Callable, Awaitable

from attrs import define, field

from .outline import Outline
from .process import Process
from .records import Message
from .threads import Thread
from src.core.broker import Envelope
from src.core.tools.search import SearchHits
from src.runtime.utils import timestamp, iso_to_epoch


SEPARATOR = "\n\n---\n\n"


@define
class ActiveContext:
    thread: Thread | None = field(default=None)
    last_n: int = field(default=4)

    async def build(self):
        if not self.thread:
            return ""
        body = await self.thread.build(self.last_n)
        return "## Active Thread\n" + body


@define
class RecentContext:
    threads: List[Thread] = field(factory=list)
    cutoff_sec: int = 60 * 60 * 6
    threads: List[Thread] = field(factory=list)

    async def build(self):
        now = timestamp()
        recents = [
            t
            for t in self.threads
            if now - iso_to_epoch(t.metadata.events[-1]["created"]()) <= self.cutoff_sec
        ][:5]
        if not recents:
            return ""
        blocks = []
        for t in recents:
            last = t.events[-1]
            blocks.append(f"[{t.id}] {last.role}: {last.content}")
        return "## Recent Threads\n" + "\n".join(blocks)


@define
class SemanticContext:
    embed: List[float] = field(factory=list)
    top_k: int = 6
    search: Callable[[List[float], int], Awaitable[SearchHits]] | None = field(
        default=None, repr=False
    )

    async def build(self):
        if not self.embed or not self.search:
            return ""
        hits = await self.search(self.embed, self.top_k)
        results = [h.get("content", "") for h in hits.hits]
        if not results:
            return ""
        return "## Semantic Search\n" + "\n".join(results)


@define
class SystemContext:
    async def build(self):
        parts = []
        parts.append("## System Info")
        parts.append(f"{timestamp()}")
        return "\n\n".join(parts)


@define
class UserContext:
    async def build(self):
        parts = []
        parts.append("## User Info")
        parts.append("Name: Tim")
        return "\n\n".join(parts)


@define
class Context:
    active: ActiveContext = field()
    recent: RecentContext = field()
    semantic: SemanticContext = field(default=SemanticContext())
    system: SystemContext = field(default=SystemContext())
    user: UserContext = field(default=UserContext())

    async def build(self):
        parts = [
            await self.system.build(),
            await self.user.build(),
            await self.active.build(),
            await self.recent.build(),
            await self.semantic.build(),
        ]
        return SEPARATOR.join(filter(None, parts))

    @singledispatchmethod
    async def update(self, obj):
        raise TypeError(f"update: unsupported type {type(obj)!r}")

    @update.register(Thread)
    async def _(self, obj):
        self.active.thread = obj
        self.recent.threads = [t for t in self.recent.threads if t.id != obj.id] + [obj]

    @update.register(Message)
    async def _(self, obj: Message):
        await self.active.thread.update(obj)

    @update.register(Outline)
    async def _(self, obj: Outline):
        await self.active.thread.update(obj)

    @update.register(Process)
    async def _(self, obj: Process):
        await self.active.thread.update(obj)

    @update.register(Envelope)
    async def _(self, obj: Envelope):
        await self.active.thread.update(obj)
