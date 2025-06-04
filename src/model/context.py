from __future__ import annotations

from functools import singledispatchmethod
from typing import List

from attrs import define, field

from src.model.records import Message
from src.model.threads import Thread
from src.runtime.utils import timestamp, iso_to_epoch


SEPARATOR = "\n\n---\n\n"


@define
class ActiveContext:
    last_n: int = field(default=4)

    async def build(self):
        pass


@define
class RecentContext:
    cutoff_sec: int = 60 * 60 * 6

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
    embed: List[float] = []
    top_k: int = 6

    async def build(self):
        pass


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
