from __future__ import annotations

from typing import Dict

from attr import field

from src.base.actor import Actor
from src.base.protocol import agentic
from src.base.types import Format
from src.interpret.continuity import Continuity
from src.interpret.context import Context
from src.base.records import Content, Instructions, Message


@agentic
class Parser(Actor):
    context: Context
    instructions: Instructions
    format: Format = Format.Message()

    async def parse(self):
        pass

    async def update(self, content: Content):
        await self.thread.update(content)
        if self.thread.metadata is None:
            self.thread.metadata = await self.generate_meta()

    async def render(self):
        parts = [self.context.Active()]
        return "\n".join(parts)


@agentic
class Observer(Actor):
    context: Context
    instructions: Instructions
    format: Format = Format.Message()

    async def parse(self):
        pass

    async def update(self, content: Content):
        await self.thread.update(content)
        if self.thread.metadata is None:
            self.thread.metadata = await self.generate_meta()

    async def render(self):
        parts = [self.context.Active()]
        return "\n".join(parts)


@agentic
class Interpreter(Actor):
    continuity: Continuity = field(default=None)
    context: Context = field(default=None)
    workers: Dict[str, Actor] = field(factory=dict)

    async def on(self, msg: Message):
        if not self.context:
            self.context = await self.continuity.resolve_thread(msg)
            await self.update(msg)
            async for res in self.interpret(msg):
                yield res

    async def interpret(self, msg: Message):
        async for res in self.generate(self.context):
            await self.update(res)
            yield res

    async def update(self, msg: Message):
        await self.context.update(msg)
