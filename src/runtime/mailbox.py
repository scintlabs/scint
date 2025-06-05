from __future__ import annotations

import asyncio
from attrs import define, field


@define
class Mailbox:
    _queue: asyncio.Queue = field(factory=asyncio.Queue)

    def empty(self) -> bool:
        return self._queue.empty()

    async def put(self, item):
        await self._queue.put(item)

    async def get(self):
        return await self._queue.get()

    def task_done(self):
        self._queue.task_done()


@define
class Envelope:
    sender: str
    model: object

    @classmethod
    def create(cls, sender: str, model: object):
        return cls(sender=sender, model=model)
