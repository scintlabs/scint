import json
from typing import List, Dict

from base.observability.logging import logger
from base.processing.messages import Message
from base.providers import OpenAIMessage
from base.persistence import LifeCycle


def deserialize_messages(messages: List[Message]) -> List[Dict[str, str | None]]:
    openai_messages: List[Dict[str, str | None]] = []

    for message in messages:
        openai_messages.append(
            {"role": message.role, "content": message.content, "name": message.name}
        )

    return json.dumps(openai_messages)  # type: ignore


def serialize_messages(openai_message: OpenAIMessage) -> Message:
    logger.info(f"Serializing message.")

    message = Message(
        role=openai_message.role,
        content=openai_message.content,
        name=openai_message.name,
        lifecycle=LifeCycle(),
    )

    return message
