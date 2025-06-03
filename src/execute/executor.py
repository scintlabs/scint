from __future__ import annotations

from attrs import field

from src.base.actor import Actor
from src.base.protocol import agentic
from src.base.types import Format
from src.execute.catalog import Catalog
from src.execute.process import Process
from src.base.records import Instructions, Message


@agentic
class Executor(Actor):
    catalog: Catalog = field(default=None)
    process: Process = field(default=None)
    instructions: Instructions = field(default=None)
    format: Format = Format.Message()

    async def on(self, msg: Message):
        if not self.context:
            self.context = await self.continuity.resolve_thread(msg)
            await self.update(msg)
            async for res in self.execute(msg):
                yield res

    async def execute(self, msg: Message):
        async for res in self.generate(self.context):
            await self.update(res)
            yield res

    async def update(self, msg: Message):
        await self.context.update(msg)

    # async def execute(self):
    #     async def sink(self):
    #         while True:
    #             try:
    #                 self.tasks.append(task)
    #             except Exception:
    #                 break

    #     sink_task = asyncio.create_task(self.sink())

    #     while not sink_task.done():
    #         while self.running and not self.queue and not sink_task.done():
    #             await asyncio.sleep(0.1)
    #         try:
    #             task = self.queue.popleft()
    #             async for res in self.generate(task):
    #                 self.context.update(res)
    #                 self.results.append(res)
    #                 yield res
    #         except Exception:
    #             break

    #     sink_task.cancel()

    #     try:
    #         await sink_task
    #     except asyncio.CancelledError:
    #         pass

    # async def update(self, query: str, limit: int = 6):
    #     res = await self.library.search_tools(query, limit)
    #     self.tools = list(res.hits)
    #     return self.tools

    # async def render(self):
    #     return [t.schema for t in self.tools]
