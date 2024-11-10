import asyncio
import json

from redis.asyncio import Redis

from scint.ensemble.traits.base import Trait


class Handler(Trait):
    async def on_event(handlers, signal):
        pass

    async def on_callback(self):
        pass

    async def handle_event(handlers, event):
        for handler in handlers.get(event, []):
            handler(event)

    def get(self, event, param):
        pass


class Publish(Trait):
    def __init__(self):
        self.url = None
        self.subscribe = None
        self.publish_channel = None
        self.publish_channel = None

    async def publish(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            r = await Redis.from_url(self.url)
            if self.subscribe:
                await r.publish(self.publish_channel, args[0].model_dump_json())
                return await self.subscribe()
            return await r.publish(self.publish_channel, args[0].model_dump_json())
        return self.__call__(*args, **kwargs)

    def __call__(self, param, param1):
        pass

    async def subscribe(self):
        pass


class Subscribe(Trait):
    def __init__(self):
        self.url = None
        self.subscribe_channel = None

    async def subscribe(self, *args, **kwargs):
        async def _reader(self, pubsub):
            while True:
                data = await pubsub.get_message(ignore_subscribe_messages=True)
                if data is not None:
                    message = json.loads(data["state"])
                    if self.callback:
                        return await self.callback(message)
                    return message

        r = await Redis.from_url(self.url)
        async with r.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe(self.subscribe_channel)
            return await asyncio.create_task(_reader(pubsub))
