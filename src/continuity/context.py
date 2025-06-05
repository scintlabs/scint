from __future__ import annotations

from attrs import define, field

from src.continuity.attention import Attention
from src.continuity.preferences import Preferences
from src.continuity.similarity import Similarity
from src.continuity.status import Status

from .threads import Threads, Thread


@define
class Context:
    attention: Attention = field()
    similarity: Similarity = field(default=Similarity())
    preferences: Preferences = field(default=Preferences())
    status: Status = field(default=Status())

    async def update(self, obj):
        self.active.thread = obj
        self.recent.threads = [t for t in self.recent.threads if t.id != obj.id] + [obj]
        await self.active.thread.update(obj)


__all__ = Context, Threads, Thread
