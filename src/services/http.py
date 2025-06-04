from __future__ import annotations

from datetime import datetime

from falcon import WebSocketDisconnected
from falcon.asgi import Request
from falcon.asgi import WebSocket


class AuthMiddleware:
    def __init__(self, protected_routes: list[str] | None = None):
        if protected_routes is None:
            protected_routes = []

        self.protected_routes = protected_routes

    async def process_request_ws(self, req: Request, ws: WebSocket):
        await ws.accept()

        if req.path not in self.protected_routes:
            return

        token = await ws.receive_text()

        if token != "very secure token":
            await ws.close(1008)
            return


class EchoWebSocketResource:
    async def on_websocket(self, req: Request, ws: WebSocket):
        while True:
            try:
                message = await ws.receive_text()
                await ws.send_media(
                    {"message": message, "date": datetime.now().isoformat()}
                )
            except WebSocketDisconnected:
                return
