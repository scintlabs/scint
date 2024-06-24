from __future__ import annotations

import asyncio
import json
import traceback

from fastapi import WebSocket, WebSocketDisconnect

from scint.messaging.router import MessageRouter
from scint.support.logging import log


class ConnectionHandler:
    def __init__(self):
        self.router = MessageRouter()
        self.connections = []
        pass

    async def connect(self):
        pass

    async def accept(self, ws: WebSocket):
        await ws.accept()

    async def receive(self, ws: WebSocket):
        message = await ws.receive_text()
        return json.loads(message)

    async def send(self, websocket, response):
        log.info(f"Sending response: {response}")
        await websocket.send_text(json.dumps(response))

    def close(self, code=None):
        pass

    def disconnect(self, code):
        pass
