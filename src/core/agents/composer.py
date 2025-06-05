from __future__ import annotations

from typing import Dict

from attrs import field

from src.model import Message, Outline, Context
from src.model.outline import Task
from src.model.records import Directions, Envelope
from src.runtime.actor import Actor
from src.runtime.protocol import agentic
from src.runtime.types import Format
from src.core.resources import Library


@agentic
class Composer(Actor):
    library: Library = field(default=None)
    context: Context = field(default=None)
    outlines: Dict[str, Outline] = field(factory=dict)
    format: Format = Format.Task()

    async def on(self, ctx: Context) -> Outline:
        """Create an outline from the provided context."""
        outline = Outline(tasks=[Task(directions=Directions(content=""))])
        self.outlines["last"] = outline
        return outline

    async def on_receive(self, env: Envelope):
        self.context = env.model
        outline = await self.on(env.model)
        if env.sender is not None:
            env.sender.tell(outline, sender=self.ref())

    async def execute(self, msg: Message):
        async for res in self.generate(self.context):
            await self.update(res)
            yield res

    async def update(self, msg: Message):
        await self.context.update(msg)
