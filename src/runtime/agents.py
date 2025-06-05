from __future__ import annotations

import asyncio
from typing import Dict

from attrs import field

from src.base.actor import Actor
from src.base.protocol import agentic
from src.base.records import Content, Instructions, Message, Outline, Process, Task
from src.continuity import Context
from src.resources.tools import ToolRepository
from src.resources.library import Library


@agentic
class Interpreter(Actor):
    _context: Context = field(default=None)
    _workers: Dict[str, Actor] = field(factory=dict)

    async def on_receive(self, env: Message):
        self._context = await self._continuity.get_context(env)
        if env.sender is not None:
            env.sender.tell(self._context, sender=self.address())

    async def interpret(self, env: Message):
        async for res in self.generate(self._context):
            await self.update(res)
            yield res

    async def update(self, env: Message):
        await self._context.update(env)


@agentic
class Composer(Actor):
    _library: Library = field(default=None)

    async def on_receive(self, context: Context):
        return await self.compose(context)

    async def compose(self, context: Context):
        outline = Outline(tasks=[Task(directions=Instructions(content=""))])
        async for outline in self.generate(context):
            self._outlines.update(outline)
            yield outline


@agentic
class Executor(Actor):
    _catalog: ToolRepository = field(default=None)
    _process: Process = field(default=None)

    async def on_receive(self, msg: Message):
        outline = msg.model
        self._process = Process(outline=outline)
        if msg.sender is not None:
            msg.sender.tell(self._process, sender=self.address())

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


@agentic
class Observer(Actor):
    _context: Context
    _instructions: Instructions

    async def observe(self):
        pass

    async def update(self, content: Content):
        await self.thread.update(content)
        if self.thread.metadata is None:
            self.thread.metadata = await self.generate_meta()

    async def render(self):
        parts = [self.context.Active()]
        return "\n".join(parts)


@agentic
class Parser(Actor):
    _context: Context
    _instructions: Instructions

    async def parse(self):
        pass

    async def update(self, content: Content):
        await self.thread.update(content)
        if self.thread.metadata is None:
            self.thread.metadata = await self.generate_meta()

    async def render(self):
        parts = [self._context.Active()]
        return "\n".join(parts)
