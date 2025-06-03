from __future__ import annotations

import asyncio

from attrs import define
from falcon.asgi.ws import WebSocket
from falcon.errors import WebSocketDisconnected

from src.base.records import Message
from src.base.broker import Broker


@define
class Socket:
    broker: Broker
    _queue: asyncio.Queue = asyncio.Queue()

    async def on_websocket(self, req, ws: WebSocket):
        try:
            await ws.accept()
            recv = asyncio.create_task(self._receiver(ws))
            send = asyncio.create_task(self._sender(ws))
            await asyncio.wait([recv, send], return_when=asyncio.FIRST_COMPLETED)
        finally:
            await ws.close()

    async def _receiver(self, ws: WebSocket):
        while True:
            try:
                data = await ws.receive_text()
                self.broker.put("interpreter", Message.create("cmd:UserInput", data))
            except WebSocketDisconnected:
                break

    async def _sender(self, ws: WebSocket):
        while True:
            msg = await self._queue.get()
            try:
                await ws.send_text(msg)
            except WebSocketDisconnected:
                break

    async def push(self, text: str):
        await self._queue.put(text)
