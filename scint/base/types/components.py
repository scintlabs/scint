from scint.base.models.messages import Message
from scint.base.models.requests import Request
from scint.base.models import parse_request, unpack_response

__all__ = "Component"

settings = {"components": [{"name": "comp_name", "module": "path"}]}


async def toggle(self, toggle: bool):
    self.running = toggle
    if self.running:
        await self.start()


async def start(self):
    while self.active:
        if self.messages.inbox:
            await self.receive()
        if self.messages.outbox:
            await self.send()


async def receive(self):
    print("Received message.")
    message = await self.messages.inbox.pop()
    await self.parse(message)


async def process_request(request: Request):
    req, method, paths = await parse_request(request)
    result = await method(**req)
    return await unpack_response(result, paths)


async def send(self, message: Message):
    print("Sending message.")
    await self.messages.push(message)
