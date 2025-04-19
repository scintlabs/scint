from __future__ import annotations

import asyncio
import json
from uuid import uuid4
from typing import Dict, List

from attrs import define, field
from redis.client import Redis

from src.core.types.activities import Activity
from src.core.types.protocols import Agent
from src.core.types.signals import Input, Output
from src.core.util.helpers import timestamp


@define(slots=True)
class Context:
    id: str = field(factory=lambda: str(uuid4()))
    input: List[Input] = field(default=list)
    output: List[Output] = field(factory=list)
    activities: Dict[str, Activity] = field(factory=list)
    protocol: Agent = field(default=None)

    async def new(self, input: Input, protocol: Agent):
        self.input = input
        self.protocol = Agent.Dialogue
        async for res in self.handle(input):
            yield res

    async def handle(self, signal: Input | Output):
        if isinstance(signal, Input):
            if signal.activity not in self.activities.keys():
                id = str(uuid4())
                activity = self.protocol.parse(id, input, self.protocol)
                self.activities[str(uuid4())] = activity
                async for res in activity:
                    yield res

        elif isinstance(signal, Output):
            self.output.append(signal)
            yield self.publish(signal)

    async def publish(self, *args):
        r = await Redis.from_url(self.url)
        if self.subscribe:
            await r.publish(self.publish_channel, args[0].model_dump_json())
            return await self.subscribe()
        return await r.publish(self.publish_channel, args[0].model_dump_json())

    async def subscribe(self, *args, **kwargs):
        async def _reader(self, pubsub):
            while True:
                data = await pubsub.get_message(ignore_subscribe_messages=True)
                if data is not None:
                    input = json.loads(data["input"])
                    yield self.handle(input)


@define
class Session:
    id: str = field(factory=lambda: str(uuid4()))
    created: str = field(factory=lambda: timestamp())
    updated: List[str] = field(factory=list)
    context: Context = Context()

    def update(self):
        self.updated.append(timestamp())

    def schedule_expiry(self):
        if self.expire_task:
            self.expire_task.cancel()
        self.expire_task = asyncio.create_task(self._expire_after())

    async def expire_after(self):
        try:
            await asyncio.sleep(900)
            await self.on_expire()
        except asyncio.CancelledError:
            pass

    async def on_expire(self):
        pass
        # await memory.encode_session(self)
        # SessionStore.delete(self.id)
