from __future__ import annotations

import asyncio
import inspect
from typing import Awaitable, Callable, Optional, Any

from attrs import define, field

from src.core.records import Envelope


class ActorExit(Exception):
    """Raise inside an actor to exit gracefully."""


@define(slots=True, frozen=True)
class Address:
    _tell: Callable[[Envelope], None] = field(repr=False)

    def tell(self, obj):
        self._tell(obj)


@define
class Mailbox:
    _address: Address = Address()
    _queue: asyncio.Queue = field(factory=lambda: asyncio.Queue(maxsize=24))

    def empty(self):
        return self._queue.empty()

    def put_nowait(self, obj: Any):
        self._queue.put_nowait(obj)

    async def put(self, obj: Any):
        await self._queue.put(obj)

    async def get(self):
        return await self._queue.get()

    def task_done(self):
        return self._queue.task_done()


@define(slots=True)
class Actor:
    _mailbox: Mailbox = Mailbox()
    _task: Optional[asyncio.Task] = field(init=False, default=None, repr=False)

    def start(self):
        if self._task is None:
            self._task = asyncio.create_task(self._runner())

    async def on_receive(self, env: Envelope) -> Awaitable[None]:
        raise NotImplementedError("override on_receive() in subclass")

    def ref(self):
        return Address(self._mailbox.put_nowait)

    async def _runner(self):
        while True:
            env = await self._mailbox.get()
            try:
                coro_or_gen = self.on_receive(env)
                if inspect.isasyncgen(coro_or_gen):
                    async for _ in coro_or_gen:
                        pass
                else:
                    await coro_or_gen
            except ActorExit:
                break
            except Exception as exc:
                print(f"{type(self).__name__} crashed: {exc}")
            finally:
                self._mailbox.task_done()
