from typing import Dict, List
from uuid import UUID, uuid4

from base.observability.logging import logger
from data.models.lifecycle import Lifecycle
from data.models.messages import Message
from data.models.metadata import Tag


def deserialize_thread(messages: List[Message]) -> List[Dict[str, str]]:
    openai_messages: List[Dict[str, str]] = []

    for message in messages:
        openai_messages.append({"role": message.role, "content": message.content})

    return openai_messages


def serialize_response(response_message) -> Message:
    logger.info(f"Serializing message: {response_message}")

    response_message = Message(
        role=response_message.role,
        content=response_message.content,
        name="Assistant",
        lifecycle=Lifecycle(),
    )

    return response_message
