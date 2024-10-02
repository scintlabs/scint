import asyncio
import json

import redis.asyncio as redis

from scint.framework.components import Component
from scint.framework.models.messages import InputMessage


class Handler(Component):
    def __init__(self):
        super().__init__()


class Subscribe(Component):
    async def evaluate(self, *args, **kwargs):
        r = await redis.from_url(self.url)
        async with r.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe(self.subscribe_channel)
            return await asyncio.create_task(self._reader(pubsub))

    async def _reader(self, pubsub):
        while True:
            data = await pubsub.get_message(ignore_subscribe_messages=True)
            if data is not None:
                message = InputMessage(**json.loads(data["data"]))
                if self.callback:
                    return await self.callback(message)
                return message


class Callback(Component):
    async def evaluate(self, *args, **kwargs):
        response = await self.callback(*args, **kwargs)
        if self.publish:
            return await self.publish(response)


class Publish(Component):
    async def evaluate(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            r = await redis.from_url(self.url)
            if self.subscribe:
                await r.publish(self.publish_channel, args[0].model_dump_json())
                return await self.subscribe()
            return await r.publish(self.publish_channel, args[0].model_dump_json())
        return self.__call__(*args, **kwargs)
