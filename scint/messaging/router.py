from __future__ import annotations
import json

from redis.asyncio import Redis

from scint.core.controller import controller
from scint.messaging.models import Message, UserMessage, AssistantMessage, SystemMessage
from scint.support.logging import log
from scint.support.utils import dictorial, keyfob


class MessageRouter:
    def __init__(self):
        self.controller = controller
        self.handlers = {}

    async def process(self, message):
        log.info(f"Processing incoming message.")
        message = validate_message(message)
        return await self.route(message)

    async def route(self, message):
        log.info(f"Routing message to context controller.")
        async for response in self.controller.process(message):
            return response

    # async def route(self, message):
    #     handlers = self.handlers.get(message.type, [])
    #     for handler in handlers:
    #         await handler.handle(message)

    # def register_handler(self, message_type, handler):
    #     if message_type not in self.handlers:
    #         self.handlers[message_type] = []
    #     self.handlers[message_type].append(handler)

    # async def publish(self, channel, message):
    #     await self.redis.publish(channel, message)

    # async def route(self, websocket, response):
    #     log.info(f"Sending response: {response}")
    #     await websocket.send_text(json.dumps(response))


message_router = MessageRouter()


def validate_message(message):
    return UserMessage(**message)
