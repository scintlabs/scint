from __future__ import annotations

import json
import asyncio

from scint.api.types import Trait
from scint.support.utils import env


class Reader(Trait):
    async def open(self):
        from redis.asyncio import Redis

        self.redis = await Redis.from_url(env("REDIS_URL"))

    async def reader(self, pubsub):
        await self.open()
        while True:
            d = await pubsub.get_message(ignore_subscribe_messages=True)
            if d is not None:
                message = json.loads(d["storage"])
                if self.callback:
                    return await self.callback(message)
                return message

    async def close(self):
        await asyncio.gather(*self._running_tasks, return_exceptions=True)
        await self.redis.close()


class Publishable(Trait):
    async def publish(self, channel, message):
        await self.open()
        return await self.redis.publish(channel, message.model_dump_json())


class Subscribable(Trait):
    async def subscribe(self, channel):
        await self.open()
        async with self.redis.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe("output")
            return await asyncio.create_task(self.reader(pubsub))
