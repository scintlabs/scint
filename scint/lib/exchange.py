from __future__ import annotations

import asyncio
from asyncio.queues import PriorityQueue
from typing import Callable

from redis.asyncio import Redis

from scint.lib.struct import Struct
from scint.lib.traits import Trait
from scint.lib.schema.signals import Event, Message

from scint.lib.util.utils import env


class Routing(Trait):
    async def route(self, routable: Message):
        try:
            await self.route_request(routable)
        except asyncio.CancelledError:
            pass

    async def route_request(self, routable: Message):
        async def sink():
            while True:
                try:
                    if isinstance(routable.content, Message):
                        await self.publish(routable.content)
                    else:
                        await self.handle_route(routable)
                except asyncio.CancelledError:
                    pass

        sink_task = asyncio.create_task(sink())

        while not sink_task.done():
            while self._requests.empty() and not sink_task.done():
                await asyncio.sleep(0.1)
            try:
                message = await self.subscribe()
                if message:
                    await self.publish(message)
                routable = await self._requests.get()
                if routable:
                    await self.handle_route(routable)
            except asyncio.CancelledError:
                pass

        sink_task.cancel()

        try:
            await sink_task
        except asyncio.CancelledError:
            pass

    async def handle_route(self, req: Message):
        if isinstance(req.content, Message):
            await self.publish(req.content)
        elif isinstance(req.content, Event):
            self._proc.put(req.content)


class Publishable(Trait):
    async def publish(self, channel: str, message: Message):
        r = await Redis.from_url(env("REDIS_URL"))
        msg = message.model_dump_json()
        await r.publish(channel, msg)
        await self.subscribe(channel)


class Subscribable(Trait):
    async def subscribe(self, channel: str, callback: Callable):
        async def _reader(pubsub):
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    callback(message["schema"].decode())

        r = await Redis.from_url(env("REDIS_URL"))
        async with r.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe(channel)
            await asyncio.create_task(_reader(pubsub))


class Exchange(Struct):
    queue = PriorityQueue()
