from __future__ import annotations

from typing import Dict

from attrs import field

from src.model import Message, Outline
from src.runtime.actor import Actor
from src.runtime.protocol import agentic
from src.runtime.types import Format
from src.core.resources import Library


@agentic
class Composer(Actor):
    library: Library = field(default=None)
    outlines: Dict[str, Outline] = field(factory=dict)
    format: Format = Format.Task()

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
