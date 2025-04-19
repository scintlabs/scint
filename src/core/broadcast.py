from __future__ import annotations

from asyncio import Queue, QueueEmpty
from typing import AsyncGenerator, Callable, Dict

from attrs import define, field

from src.core.types.context import Session
from src.core.types.signals import Signal
from src.core.types.ensemble import Ensemble
from src.core.util.llms import embedding


@define
class Broadcast:
    sessions: Dict[str, Session] = field(factory=dict)
    subscribers: Dict[str, Ensemble] = field(factory=dict)
    queue: Queue = Queue()

    def subscribe(self, name: str, handle: Callable[[Session, Signal], AsyncGenerator]):
        self.subscribers[name] = handle

    def session(self, sid: str | None):
        if sid in self.sessions and not self.sessions[sid].expired():
            return self.sessions[sid]
        self.sessions[sid] = Session()
        return self.sessions[sid]

    async def input(self, input: Signal):
        input.embedding = embedding(input.content)
        await self.queue.put(input)
        async for res in self.dispatch():
            yield res

    async def output(self, output: Signal):
        pass

    async def dispatch(self, sid: str | None = None):
        while not self.queue.empty():
            try:
                signal = await self.queue.get()
                handle = self.subscribers["Persona"]
                try:
                    async for res in handle(signal):
                        yield res
                except Exception as e:
                    print(f"Error in handler: {e}")

                self.queue.task_done()

            except QueueEmpty:
                break
            except Exception as e:
                print(f"Error dispatching signal: {e}")
                self.queue.task_done()
