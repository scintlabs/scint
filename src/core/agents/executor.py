from __future__ import annotations
import asyncio

from attrs import field

from src.core.resources import Catalog
from src.model.outline import Outline
from src.model.process import Process
from src.runtime.actor import Actor
from src.runtime.protocol import agentic


@agentic
class Executor(Actor):
    _catalog: Catalog = field(default=None)
    _process: Process = field(default=None)

    async def on_receive(self, out: Outline):
        if not self.context:
            self.context = await self.continuity.resolve_thread(out)
            await self.update(out)
            async for res in self.execute(out):
                yield res

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
