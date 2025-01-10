import json
import asyncio
from collections import deque

from redis.asyncio import Redis
from websockets import WebSocketException


class Broker:
    def __init__(self):
        super().__init__()
        self.messages = deque()

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
                    message = json.loads(data["storage"])
                    if self.callback:
                        return await self.callback(message)
                    return message

        r = await Redis.from_url(self.url)
        async with r.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe(self.subscribe_channel)
            return await asyncio.create_task(_reader(pubsub))

    async def on_websocket(self, req, ws):
        try:
            await ws.accept()
            await self.process_websocket(req)
        except WebSocketException:
            await ws.close()

    async def process_websocket(self, req):
        async def sink(self, req):
            while True:
                try:
                    self.queue.append(req)
                except Exception:
                    break

        sink_task = asyncio.create_task(self.sink())

        while not sink_task.done():
            while self.running and not self.queue and not sink_task.done():
                await asyncio.sleep(0.1)
            try:
                await self.handler(self.queue.popleft())
            except Exception:
                break

        sink_task.cancel()

        try:
            await sink_task
        except asyncio.CancelledError:
            pass
