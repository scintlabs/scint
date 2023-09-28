from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.persistence import LifeCycle
from base.processing import Tag


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    role: str
    content: str
    name: str | None


class PersistedMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    message_id: UUID
    lifecycle: LifeCycle
    topic: List[Tag]
    content_summary: str


class MessageThread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    messages: List[Message | PersistedMessage]
    topic: List[Tag]


class PersistedMessageThread(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    thread_id: UUID
    lifecycle: LifeCycle
    topic: List[Tag]
    content_summary: str
