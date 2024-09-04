import asyncio
import json

from scint.core.components import Component
from scint.core.primitives.messages import InputMessage


__all__ = "Handler"


class Handler(Component):
    def __init__(self, channels, embedding, input, output, callback=None):
        self.channels = channels
        self.embedding = embedding
        self.input = input
        self.output = output
        self.callback = callback
        self.start()

    def start(self):
        asyncio.gather(asyncio.create_task(self.subscribe()))

    async def subscribe(self):
        message = await self.channels.subscribe(self.input)
        if self.callback is not None:
            await self.prepare(message["data"])
        else:
            await self.publish(message["data"])

    async def prepare(self, message):
        msg = InputMessage(**json.loads(message))
        if msg.embedding is None:
            msg.embedding = await self.embedding(msg.sketch)
        res = await self.callback(msg)
        await self.publish(res.model_dump_json())

    async def publish(self, message):
        await self.channels.publish(self.output, message)
        await self.subscribe()
