from __future__ import annotations

import asyncio
import operator
from collections import deque
from functools import reduce

import redis.asyncio as redis
from falcon.asgi.ws import falcon
from falcon.asgi import Request, WebSocket
from falcon.errors import WebSocketDisconnected, WebSocketServerError

from scint.base.components.prompts.prompts import Block
from scint.base.utils import dictorial


async def redis_subscribe(channel):
    async def _reader(channel):
        while True:
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message is not None:
                return message

    try:
        r = await redis.from_url("redis://localhost")
        async with r.pubsub() as pubsub:
            await pubsub.subscribe(channel)
            return await asyncio.create_task(_reader(pubsub))
    except (Exception, WebSocketServerError) as e:
        print(e)


async def redis_publish(channel, message):
    try:
        r = await redis.from_url("redis://localhost")
        await r.publish(channel, message)
    except (Exception, WebSocketServerError) as e:
        print(e)


class MessageBus:
    def __init__(self, host, port):
        print("Starting messaging.")
        self.messages = deque()
        task = asyncio.create_task(self.subscribe())
        asyncio.gather(task)

    async def on_websocket(self, req: Request, ws: WebSocket):
        try:
            await ws.accept()
        except WebSocketDisconnected:
            await ws.close()

        async def sink():
            while True:
                try:
                    message = await ws.receive_text()
                    await self.publish_message(message)
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
            except WebSocketDisconnected:
                break

        sink_task.cancel()

        try:
            await sink_task
        except asyncio.CancelledError:
            pass

    async def subscribe(self):
        try:
            message = await redis_subscribe("output")
            if message:
                print(f"Sockets: message received from system: {message}")
                self.messages.append(message["data"].decode())
        except (Exception, WebSocketServerError) as e:
            print(e)

    async def publish_message(self, message):
        try:
            await redis_publish("input", message)
        except (Exception, WebSocketServerError) as e:
            print(e)


class Multiplex(dict):
    def __init__(self, objs=[]):
        dict.__init__(self)
        for alias, obj in objs:
            self[alias] = obj

    def __call__(self, *args, **kwargs):
        # Call registered objects and return results through another Multiplex.
        return self.__class__(
            [(alias, obj(*args, **kwargs)) for alias, obj in self.items()]
        )

    def __nonzero__(self):
        # A Multiplex is true if all registered objects are true.
        return reduce(operator.and_, self.values(), 1)

    def __getattr__(self, name):
        # Wrap requested attributes for further processing."""
        try:
            return dict.__getattribute__(self, name)
        except:
            # Return another Multiplex of the requested attributes
            return self.__class__(
                [(alias, getattr(obj, name)) for alias, obj in self.items()]
            )
