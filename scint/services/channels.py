from __future__ import annotations

import asyncio
from collections import deque

import redis.asyncio as redis

from falcon.asgi import Request, WebSocket
from falcon.asgi.ws import falcon
from falcon.errors import WebSocketDisconnected

from scint.services import Service


class Channels(Service):
    def __init__(self, context):
        super().__init__()
        self.context = context.create("channels")
        self.context.publish = self.publish
        self.context.subscribe = self.subscribe
        self.messages = deque()

    async def on_websocket(self, req: Request, ws: WebSocket):
        try:
            await ws.accept()
        except WebSocketDisconnected:
            await ws.close()

        async def sink():
            while True:
                try:
                    message = await ws.receive_text()
                    await self.publish("input", message)
                    await self.subscribe("output")
                except WebSocketDisconnected:
                    break
                except Exception as e:
                    print(e)

        sink_task = falcon.create_task(sink())
        while not sink_task.done():
            while ws.ready and not self.messages and not sink_task.done():
                await asyncio.sleep(0.1)

            try:
                await ws.send_text(self.messages.popleft())
                await self.subscribe("output")
            except WebSocketDisconnected:
                break

        sink_task.cancel()

        try:
            await sink_task
        except asyncio.CancelledError:
            pass

    async def publish(self, channel, message):
        try:
            r = await redis.from_url("redis://localhost")
            await r.publish(channel, message)
        except Exception as e:
            print(e)

    async def subscribe(self, channel):
        async def _reader(channel):
            while True:
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    return message

        try:
            r = await redis.from_url("redis://localhost")
            async with r.pubsub() as pubsub:
                if not pubsub.subscribed:
                    await pubsub.subscribe(channel)
                return await asyncio.create_task(_reader(pubsub))
        except Exception as e:
            print(e)
