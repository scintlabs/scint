from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.core.agents.dispatcher import Dispatcher
from src.model.records import Message, Envelope
from src.runtime.actor import Actor


class WebSocketActor(Actor):
    def __init__(self, ws: WebSocket):
        super().__init__()
        self._ws = ws

    async def on_receive(self, env: Envelope):
        data = env.model
        if isinstance(data, Message):
            content = data.content
        else:
            content = data
        if isinstance(content, bytes):
            await self._ws.send_bytes(content)
        else:
            await self._ws.send_text(str(content))


def create_app() -> FastAPI:
    app = FastAPI()
    dispatcher = Dispatcher()

    @app.on_event("startup")
    async def startup_event() -> None:
        dispatcher.load()
        dispatcher.start()

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        actor = WebSocketActor(ws)
        actor.start()
        try:
            while True:
                try:
                    message = await ws.receive()
                except WebSocketDisconnect:
                    break
                if "text" in message and message["text"] is not None:
                    msg = Message(content=message["text"])
                elif "bytes" in message and message["bytes"] is not None:
                    msg = Message(content=message["bytes"])
                else:
                    continue
                env = Envelope.create("user", msg)
                dispatcher.ref().tell(env, sender=actor.ref())
        finally:
            if actor._task:
                actor._task.cancel()

    return app
