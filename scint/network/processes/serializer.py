import datetime
import json
from dataclasses import asdict
from uuid import UUID

from scint.repository.models.message import Footer, Header, Message, Payload


class MessageSerializer:
    @staticmethod
    def serialize(message: Message) -> str:
        def serialize_uuid(obj):
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        message_dict = asdict(message)
        return json.dumps(message_dict, default=serialize_uuid)

    @staticmethod
    def deserialize(message_str: str) -> Message:
        message_dict = json.loads(message_str)
        headers = Header(**message_dict["headers"])
        payload = Payload(**message_dict["payload"])
        footer = (
            Footer(**message_dict["footer"]) if message_dict.get("footer") else None
        )

        return Message(headers=headers, payload=payload, footer=footer)
