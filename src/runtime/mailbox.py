from __future__ import annotations

import asyncio
from typing import Any

from attrs import define, field


@define(slots=True)
class Envelope:
    """Simple wrapper for actor messages."""
    model: Any = field(default=None)
    sender: str | None = field(default=None)
    metadata: Any = field(default=None)
    correlation: str | None = field(default=None)

    @classmethod
    def create(cls, sender: str, model: Any):
        return cls(model=model, metadata=None, sender=sender)


@define
class Mailbox:
    """Simple async message queue used by actors."""
    _queue: asyncio.Queue = field(factory=lambda: asyncio.Queue(maxsize=24))

    def empty(self) -> bool:
        return self._queue.empty()

    def put_nowait(self, obj: Any) -> None:
        self._queue.put_nowait(obj)

    async def put(self, obj: Any) -> None:
        await self._queue.put(obj)

    async def get(self) -> Envelope:
        return await self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()


__all__ = ["Mailbox", "Envelope"]
