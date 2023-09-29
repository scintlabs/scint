from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.observability.logging import logger
from base.persistence.lifecycle import LifeCycle
from base.processing import Tag


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    role: str
    content: str
    name: str


class PersistedMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    message_id: UUID
    lifecycle: LifeCycle
    topics: List[Tag]
    content_summary: str


class MessageThread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    messages: List[Message | PersistedMessage]
    topics: List[Tag]


class PersistedMessageThread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    thread_id: UUID
    lifecycle: LifeCycle
    topics: List[Tag]
    content_summary: str


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
        lifecycle=LifeCycle(),
    )

    return response_message
