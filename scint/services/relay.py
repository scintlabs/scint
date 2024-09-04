from __future__ import annotations

import asyncio
from collections import deque

from falcon.asgi import Request, WebSocket
from falcon.asgi.ws import falcon
from falcon.errors import WebSocketDisconnected, WebSocketServerError

from scint.services import Service


class Relay(Service):
    def __init__(self, context):
        super().__init__()
        self.context = context
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
                    await self.publish(message)
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
            message = await self.context.channels.subscribe("output")
            if message:
                print(f"Sockets: message received from system: {message}")
                self.messages.append(message["data"].decode())
        except (Exception, WebSocketServerError) as e:
            print(e)

    async def publish(self, message):
        try:
            await self.context.channels.publish("input", message)
            await self.subscribe()
        except (Exception, WebSocketServerError) as e:
            print(e)
