from typing import List

from scint.network.processors.middleware import MessageMiddleware
from scint.repository.models.message import Message


class MessageProcessor:
    def process_message(self, message: Message): ...


class MessagePipeline:
    def __init__(self, middlewares: List[MessageMiddleware]):
        self.middlewares = middlewares

    def process(self, message: Message):
        for middleware in self.middlewares:
            message = middleware.process(message)
        return message
