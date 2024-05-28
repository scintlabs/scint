from __future__ import annotations

import asyncio
import json
import traceback

from fastapi import WebSocket, WebSocketDisconnect
from redis.asyncio import Redis

from scint.core.controller import controller
from scint.modules.logging import log
from scint.core.models import Message, UserMessage
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
            message.embedding = dictorial(result, "choices.0.data.embedding")
            return message
        except Exception as e:
            log.error(f"Error embedding message: {e}")

    async def route_message(self, message: Message):
        try:
            log.info(f"Routing message to context controller.")
            prepared_message = await self.prepare_message(message)
            result = self.controller.contextualize(prepared_message)
            async for message in result:
                yield message
        except Exception as e:
            log.error(f"Error routing message: {e}\n{traceback.format_exc()}")

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
        redis_listener = None
        heartbeat_interval = 30
        try:
            redis_listener = asyncio.create_task(self.websocket_listener(websocket))
            while True:
                try:
                    await websocket.send_json({"type": "ping"})
                    pong_waiter = await asyncio.wait_for(
                        websocket.receive_json(), timeout=heartbeat_interval
                    )
                    if pong_waiter.get("type") != "pong":
                        log.warning("Did not receive pong response, reconnecting...")
                        raise WebSocketDisconnect
                    message = await asyncio.wait_for(
                        self.receive(websocket), timeout=heartbeat_interval
                    )
                    await self.publish(self.channel, json.dumps(message))
                except asyncio.TimeoutError:
                    log.warning("Ping timeout, reconnecting...")
                    raise WebSocketDisconnect
        except WebSocketDisconnect:
            log.info("WebSocket disconnected")
        except Exception as e:
            log.error(f"Exception: {e}\n{traceback.format_exc()}")
        finally:
            if redis_listener:
                redis_listener.cancel()
            await websocket.close()
            if self.pubsub:
                await self.pubsub.unsubscribe(self.channel)
                await self.pubsub.close()
            await self.redis.close()
            log.info("Closed WebSocket and Redis connections gracefully.")


message_queue = MessageQueue()
