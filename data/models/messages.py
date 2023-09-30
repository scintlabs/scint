from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.observability.logging import logger
from base.processing import Tag
from data.models.lifecycle import Lifecycle


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: Lifecycle
    role: str
    content: str
    name: str


class PersistedMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    message_id: UUID
    lifecycle: Lifecycle
    topics: List[Tag]
    content_summary: str


class MessageThread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: Lifecycle
    messages: List[Message | PersistedMessage]
    topics: List[Tag]


class PersistedMessageThread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    thread_id: UUID
    lifecycle: Lifecycle
    topics: List[Tag]
    content_summary: str
