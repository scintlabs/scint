from __future__ import annotations
from typing import Dict

from attrs import field

from src.runtime.actor import Actor
from src.runtime.protocol import agentic
from src.model.records import Content, Instructions, Envelope
from src.model.context import Context
from src.core.resources.continuity import Continuity


@agentic
class Interpreter(Actor):
    _continuity: Continuity = field(default=None)
    _context: Context = field(default=None)
    _workers: Dict[str, Actor] = field(factory=dict)

    async def on_receive(self, env: Envelope):
        self._context = await self._continuity.get_context(env)
        if env.sender is not None:
            env.sender.tell(self._context, sender=self.ref())

    async def interpret(self, env: Envelope):
        async for res in self.generate(self._context):
            await self.update(res)
            yield res

    async def update(self, env: Envelope):
        await self._context.update(env)


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
