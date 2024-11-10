import datetime
from abc import ABC, abstractmethod
from dataclasses import replace


from scint.repository.models.message import Message


class MessageMiddleware(ABC):
    @abstractmethod
    def process(self, message: Message):
        pass


class ValidationMiddleware(MessageMiddleware):
    def process(self, message: Message) -> Message:
        assert message.headers.message_type
        assert message.payload.content
        return message


class EnrichmentMiddleware(MessageMiddleware):
    def process(self, message: Message) -> Message:
        new_headers = replace(
            message.headers,
            custom_headers={
                **message.headers.custom_headers,
                "enriched_at": datetime.utcnow().isoformat(),
            },
        )
        return replace(message, headers=new_headers)
