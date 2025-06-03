from __future__ import annotations

import asyncio
from typing import Optional

from attrs import define, field

from src.base.records import Message, Command


class ActorExit(Exception):
    """Raise inside an actor to terminate it gracefully."""


@define(slots=True)
class Actor:
    _task: Optional[asyncio.Task] = field(default=None)
    _inbox: asyncio.Queue = field(factory=lambda: asyncio.Queue(maxsize=24))
    _outbox: asyncio.Queue = field(factory=lambda: asyncio.Queue(maxsize=24))

    def put(self, msg: Message):
        self._inbox.put_nowait(msg)

    async def ask(self, msg: Message):
        self._inbox.put_nowait(msg)
        await self.start()
        return await asyncio.wait_for(self._outbox.get(), timeout=60)

    async def on(self, msg: Message):
        raise NotImplementedError("Subclasses must implement on()")

    async def start(self):
        if not self._task:
            self._task = asyncio.create_task(self._run())

    async def stop(self):
        stop_cmd = Command("_stop")
        self._inbox.put_nowait(stop_cmd)
        if self._task:
            await self._task

    async def _run(self):
        try:
            while True:
                try:
                    msg = await self._inbox.get()
                    handler = self.on(msg)
                    async for res in handler:
                        await self._outbox.put(res)
                except Exception as e:
                    if self._outbox:
                        await self._outbox.put(e)

                self._inbox.task_done()
        except ActorExit:
            pass
        except Exception as e:
            print(f"Actor {self.__class__.__name__} crashed: {e}")

    async def spawn(self, actor_cls: Actor, *args, **kwargs):
        actor = actor_cls(self, *args, **kwargs)
        await actor.start()
        return actor
