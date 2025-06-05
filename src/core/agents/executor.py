from __future__ import annotations
import asyncio

from attrs import field

from src.core.resources import Catalog
from src.model.process import Process
from src.model.records import Envelope
from src.runtime.actor import Actor
from src.runtime.protocol import agentic


@agentic
class Executor(Actor):
    _catalog: Catalog = field(default=None)
    _process: Process = field(default=None)

    async def on_receive(self, env: Envelope):
        outline = env.model
        self._process = Process(outline=outline)
        if env.sender is not None:
            env.sender.tell(Envelope(model=self._process), sender=self.ref())

    async def execute(self):
        async def sink(self):
            while True:
                try:
                    self.tasks.append(task)
                except Exception:
                    break

        sink_task = asyncio.create_task(self.sink())

        while not sink_task.done():
            while self.running and not self.queue and not sink_task.done():
                await asyncio.sleep(0.1)
            try:
                task = self.queue.popleft()
                async for res in self.generate(task):
                    self.context.update(res)
                    self.results.append(res)
                    yield res
            except Exception:
                break

        sink_task.cancel()

        try:
            await sink_task
        except asyncio.CancelledError:
            pass

    async def update(self, query: str, limit: int = 6):
        res = await self.library.search_tools(query, limit)
        self.tools = list(res.hits)
        return self.tools

    async def render(self):
        return [t.schema for t in self.tools]
