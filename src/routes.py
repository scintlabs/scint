from __future__ import annotations

from attrs import define, field
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.base.actor import Actor
from src.base.records import Message
from src.runtime.system import System, Envelope


@define
class WebSocketActor(Actor):
    _ws: WebSocket = field(init=False)

    def __attrs_post_init__(self, ws: WebSocket):
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
    sys = System()
    sys.start()

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
                sys.address().tell(env, sender=actor.address())
        finally:
            if actor._task:
                actor._task.cancel()

    return app
