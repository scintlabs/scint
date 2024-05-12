from scint.base.modules.components.component import ComponentType
from scint.support.types import Context, Message
from scint.support.logging import log


class Interface(metaclass=ComponentType):
    """
    The interface communicates with the user.

    You are a natural language interface designed to communicate with the user. You receive user messages and system messages. For user messages, respond normally. For system messages, communicate the content to the user, but don't inform them there's a separate system message—present a unified interface.
    """

    async def parse(self, message: Message):
        log.info(f"{self.name} is parsing a message: {message}")
        self.messages.append(message)
        metadata = self.metadata
        async for response in self.intelligence.parse(Context(**metadata)):
            yield response


class ScintInterface(Interface):
    pass
