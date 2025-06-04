from __future__ import annotations

import asyncio
import inspect
from typing import Awaitable, Callable, Optional

from attrs import define, field

from src.runtime.mailbox import Envelope, Mailbox


@define(slots=True, frozen=True)
class ActorRef:
    _tell: Callable[[Envelope], None] = field(repr=False)

    def tell(self, model, sender: ActorRef | None = None):
        self._tell(Envelope(model=model, sender=sender))


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
        return ActorRef(self._mailbox.put_nowait)

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


class ActorExit(Exception):
    """Raise inside an actor to exit gracefully."""


# @define
# class Actor:
#     _mailbox: Mailbox = Mailbox()

#     def tell(self, envelope: Envelope):
#         self._inbox.put_nowait(envelope)

#     async def spawn(self, actor_cls: Actor, *args, **kwargs):
#         actor = actor_cls(self, *args, **kwargs)
#         await actor.start()
#         return actor

#     async def ask(self, envelope: Envelope):
#         self._inbox.put_nowait(envelope)
#         await self.start()
#         return await asyncio.wait_for(self._outbox.get(), timeout=60)

#     async def on(self, envelope: Envelope):
#         raise NotImplementedError("Subclasses must implement on()")

#     async def start(self):
#         if not self._task:
#             self._task = asyncio.create_task(self._run())

#     async def stop(self):
#         pass

#     async def _run(self):
#         try:
#             while True:
#                 try:
#                     msg = await self._inbox.get()
#                     handler = self.on(msg)
#                     async for res in handler:
#                         await self._outbox.put(res)
#                 except Exception as e:
#                     if self._outbox:
#                         await self._outbox.put(e)

#                 self._inbox.task_done()
#         except ActorExit:
#             pass
#         except Exception as e:
#             print(f"Actor {self.__class__.__name__} crashed: {e}")
