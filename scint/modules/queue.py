from __future__ import annotations

import asyncio
import json
import traceback

from fastapi import WebSocket, WebSocketDisconnect
from redis.asyncio import Redis

from scint.core.controller import controller
from scint.modules.logging import log
from scint.data.schema import Message, UserMessage
from scint.settings import intelligence
from scint.data.serialize import dictorial


class MessageQueue:
    def __init__(self, host="localhost", port=6379):
        self.redis = Redis(host=host, port=port)
        self.pubsub = None
        self.channel = "context"
        self.controller = controller

    async def connect(self, retries=5, delay=2):
        for attempt in range(retries):
            try:
                self.pubsub = self.redis.pubsub()
                await self.pubsub.subscribe(self.channel)
                log.info("Successfully connected to Redis.")
                break
            except Exception as e:
                log.error(
                    f"Redis connection failed: {e}. Retrying in {delay} seconds..."
                )
                await asyncio.sleep(delay)
        else:
            log.error("Failed to connect to Redis after multiple attempts.")

    async def publish(self, channel, message):
        await self.redis.publish(channel, message)

    async def receive(self, websocket):
        message = await websocket.receive_text()
        return json.loads(message)

    async def send(self, websocket, response):
        log.info(f"Sending response: {response}")
        await websocket.send_text(json.dumps(response))

    async def prepare_message(self, message: Message):
        log.info(f"Preparing message.")
        try:
            provider = dictorial(intelligence, "providers.openai")
            method = dictorial(provider, "format.embedding.method")
            result = await method(model="text-embedding-3-small", input=message.content)
            message.embedding = dictorial(result, "data.0.embedding")
            return message
        except Exception as e:
            log.error(f"Error embedding message: {e}")

    async def route_message(self, message: Message):
        try:
            log.info(f"Routing message to context controller.")
            prepared_message = await self.prepare_message(message)
            if prepared_message:
                result = self.controller.contextualize(prepared_message)
                async for message in result:
                    yield message
            else:
                log.warning("Prepared message is None, skipping routing")
        except Exception as e:
            log.error(f"Error routing message: {e}\n{traceback.format_exc()}")

    async def websocket_listener(self, websocket: WebSocket):
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                log.info(f"Received: {message['data'].decode()}")
                try:
                    message_data = json.loads(message["data"])
                    if "content" in message_data and message_data["content"].strip():
                        user_message = UserMessage(content=message_data["content"])
                        async for res in self.route_message(user_message):
                            response = {"role": res.role, "content": str(res.content)}
                            await self.send(websocket, response)
                    else:
                        log.warning("Received empty message content")
                except json.JSONDecodeError:
                    log.error("Failed to decode JSON message")

    async def websocket_handler(self, websocket: WebSocket):
        await websocket.accept()
        await self.connect()
        redis_listener = None
        heartbeat_interval = 30
        try:
            redis_listener = asyncio.create_task(self.websocket_listener(websocket))
            while True:
                try:
                    message = await asyncio.wait_for(
                        self.receive(websocket),
                        timeout=heartbeat_interval,
                    )
                    if message.get("type") == "heartbeat":
                        await websocket.send_text(
                            json.dumps({"type": "heartbeat", "content": "ping"})
                        )
                    else:
                        await self.publish(self.channel, json.dumps(message))
                except asyncio.TimeoutError:
                    await websocket.send_text(
                        json.dumps({"type": "heartbeat", "content": "ping"})
                    )
        except WebSocketDisconnect:
            log.info("WebSocket disconnected")
        except Exception as e:
            log.error(f"Exception: {e}\n{traceback.format_exc()}")
        finally:
            if redis_listener:
                redis_listener.cancel()


message_queue = MessageQueue()
