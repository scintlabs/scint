from __future__ import annotations

import asyncio
import json
import traceback

from redis.asyncio import Redis

from scint.messaging.models import Message, UserMessage
from scint.messaging.router import message_router
from scint.support.logging import log
from scint.support.types import WebSocket, WebSocketDisconnect
from scint.support.utils import dictorial


class MessageQueue:
    def __init__(self, host="localhost", port=6379):
        self.redis = Redis(host=host, port=port)
        self.pubsub = self.redis.pubsub()
        self.channel = "context"
        self.message_router = message_router

    async def connect(self):
        await self.pubsub.subscribe(self.channel)
        log.info("Successfully connected to Redis.")

    async def publish(self, channel, message):
        await self.redis.publish(channel, message)

    async def receive(self, websocket):
        message = await websocket.receive_text()
        return json.loads(message)

    async def send(self, websocket, response):
        log.info(f"Sending response: {response}")
        await websocket.send_text(json.dumps(response))

    async def route_message(self, message: Message):
        log.info(f"Routing message to context controller.")
        response = await self.message_router.process(message)
        return response

    async def websocket_listener(self, websocket: WebSocket):
        async for pub in self.pubsub.listen():
            log.info(f"Message received.")
            try:
                message = json.loads(pub["data"])
                await self.send(websocket, await self.route_message(message))
            except Exception as e:
                log.error(e)

    async def websocket_handler(self, ws: WebSocket):
        await ws.accept()
        await self.connect()
        redis_listener = None
        ping = json.dumps({"type": "heartbeat", "content": "ping"})
        try:
            redis_listener = asyncio.create_task(self.websocket_listener(ws))
            while True:
                try:
                    message = await self.receive(ws)
                    if message.get("type") == "heartbeat":
                        await ws.send_text(ping)
                    else:
                        await self.publish(self.channel, json.dumps(message))
                except asyncio.TimeoutError:
                    await ws.send_text(ping)
        except WebSocketDisconnect:
            log.info("WebSocket disconnected")
        except Exception as e:
            log.error(f"Exception: {e}\n{traceback.format_exc()}")
        finally:
            if redis_listener:
                redis_listener.cancel()


message_queue = MessageQueue()
