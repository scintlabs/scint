from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    role: Role


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Entity
    content: str


class Function(BaseModel):
    pass
