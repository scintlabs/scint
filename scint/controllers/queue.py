from __future__ import annotations

import asyncio
import json
import traceback

from redis.asyncio import Redis
from fastapi import WebSocket, WebSocketDisconnect

from scint.support.logging import log
from scint.support.types import Message, UserMessage
from scint.controllers.context import context_controller


class MessageQueue:
    """ """

    def __init__(self, host="localhost", port=6379):
        self.redis = Redis(host=host, port=port)
        self.pubsub = None
        self.channel = "requests"
        self.controller = context_controller

    async def connect(self):
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(self.channel)

    async def publish(self, channel, message):
        await self.redis.publish(channel, message)

    async def receive(self, websocket):
        message = await websocket.receive_text()
        return json.loads(message)

    async def send(self, websocket, response):
        await websocket.send_text(json.dumps(response))

    async def route_message(self, message):
        log.info(f"Routing message to context controller.")
        response_generator = self.controller.process(message)
        async for result in response_generator:
            yield result

    async def websocket_listener(self, websocket: WebSocket):
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                log.info(f"Received: {message['data'].decode()}")
                message = json.loads(message["data"])
                message = UserMessage(content=message["content"])
                async for res in self.route_message(message):
                    response = {"role": res.role, "content": str(res.content)}
                    await self.send(websocket, response)

    async def websocket_handler(self, websocket: WebSocket):
        await websocket.accept()
        await self.connect()
        try:
            redis_listener = asyncio.create_task(self.websocket_listener(websocket))

            while True:
                message = await self.receive(websocket)
                await self.publish(self.channel, json.dumps(message))

        except WebSocketDisconnect:
            log.info("WebSocket disconnected")
        except Exception as e:
            traceback_details = traceback.format_exc()
            log.error(f"Exception: {e}\n{traceback_details}")
        finally:
            redis_listener.cancel()


message_bus = MessageQueue()
