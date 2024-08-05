import asyncio
import json
from functools import wraps

import redis.asyncio as redis
from falcon.errors import WebSocketServerError

from scint.base.components.containers.queue import Queues
from scint.base.components.emitters.emitter import EmitterType
from ..functions.function import Functions

from ..containers import Queue
from ..functions.function import Function
from scint.base.components.prompts.prompts import Message, Messages
from scint.base.requests.process import process_request
from scint.base.requests.schema import Request
from scint.base.utils import generate_id


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


class Interface(metaclass=EmitterType):
    def __init__(self):
        super().__init__()
        task = asyncio.create_task(self.subscribe())
        asyncio.gather(task)

    async def subscribe(self):
        message = await redis_subscribe("input")
        if message:
            print(f"System: message received from sockets: {message}")
            await self.process_message(message["data"].decode())

    async def process_message(self, message: Message):
        print("Processing message.")
        response = await self.process(Message(**json.loads(message)))
        await self.publish_message(response)

    async def publish_message(self, message):
        await redis_publish("output", message.model_dump_json())
        await self.subscribe()


class Router(metaclass=EmitterType):
    def __init__(self, context, **kwargs):
        super().__init__()

    async def route(self, message: Messages):
        message = await self.queues.inbox.get(message)
        await self.parse(message)

    def send_message(self, sender_id, user_id, message):
        if user_id in self.users:
            user = self.users[user_id]
            user.receive_message(sender_id, message)
        else:
            print(f"User {user_id} not found.")
