from __future__ import annotations

import asyncio

from attrs import define, field

from src.model import Model, Metadata


@define(slots=True)
class Envelope:
    model: Model = field(default=None)
    sender: str = field(default=None)
    metadata: Metadata = field(default=None)
    correlation: str = field(default=None)

    @classmethod
    def create(cls, sender: str, model: Model):
        return cls(model=model, metadata=Metadata())


@define
class Mailbox:
    _queue: asyncio.Queue = field(factory=lambda: asyncio.Queue(maxsize=24))

    def empty(self):
        return self._queue.empty()

    def put_nowait(self, env: Envelope):
        self._queue.put_nowait(env)

    async def put(self, env: Envelope):
        await self._queue.put(env)

    async def get(self):
        return await self._queue.get()

    def task_done(self):
        return self._queue.task_done()
