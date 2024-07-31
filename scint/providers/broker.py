import json
import traceback

from falcon.asgi.app import Request, WebSocket, WebSocketDisconnected

from scint.base.models.messages import Block, Message
from scint.base.types.providers import ProviderType
from scint import Settings

settings = Settings()
settings.load_json("settings/providers.json", "providers")


class MessageBroker(metaclass=ProviderType):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.context = None

    async def on_websocket(self, req: Request, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)
        await self.websocket_listener(ws)

    async def websocket_listener(self, ws: WebSocket):
        try:
            while True:
                message = await ws.receive_text()
                await self.process(json.loads(message))

        except WebSocketDisconnected:
            self.connections.remove(ws)
            print("Websocket disconnected.")
        except Exception as e:
            print(f"Websocket exception: {e}\n{traceback.format_exc()}.")

    async def receive(self, ws: WebSocket):
        print("Message received.")
        return await ws.receive_text()

    async def process(self, message):
        print(f"Processing incoming message.")
        blocks = []
        for block in message.get("items"):
            blocks.append(Block(**block))
        message = Message(sender="user", receiver="any", body=blocks)
        return await self.context.send(message)

    async def send(self, ws: WebSocket, res):
        print(f"Sending response: {res}")
        return await ws.send_text(res)

    async def close_connection(self, ws: WebSocket):
        if ws in self.connections:
            await ws.close()
            self.connections.remove(ws)
            print("Connection manually closed.")
