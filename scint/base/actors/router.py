from scint.base.models.messages import Message
from scint.base.types.actors import ActorType


class Router(metaclass=ActorType):
    def __init__(self, context, **kwargs):
        super().__init__()
        self.children = []

    async def route(self, message: Message):
        message = await self.queues.inbox.get(message)
        await self.parse(message)
