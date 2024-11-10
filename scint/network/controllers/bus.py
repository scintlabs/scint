from typing import Callable, Dict, List

from scint.network.processors.message import MessagePipeline
from scint.repository.models.message import Message


class MessageBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.pipeline = MessagePipeline([])

    def register_handler(self, message_type: str, handler: Callable):
        if message_type not in self.handlers:
            self.handlers[message_type] = []
        self.handlers[message_type].append(handler)

    def publish(self, message: Message):
        processed_message = self.pipeline.process(message)
        message_type = processed_message.headers.message_type
        if message_type in self.handlers:
            for handler in self.handlers[message_type]:
                handler(processed_message)
