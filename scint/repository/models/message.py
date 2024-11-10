from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Generic, List, Optional, TypeVar
from uuid import uuid4

from scint.ensemble.components.enum import Enumerator
from scint.repository.models.base import Model

T = TypeVar("T")


def identifier() -> str:
    return str(uuid4())


def timestamp() -> str:
    return str(datetime.now(timezone.utc).strftime("%Y-%m-%d  %H:%M:%S"))


Blocks = Enumerator(
    TEXT=type("Text", (), {}),
    CODE=type("Code", (), {}),
    IMAGE=type("Image", (), {}),
    LINK=type("Link", (), {}),
    VECTOR=type("Vector", (), {}),
)


@dataclass
class Block(Model):
    type = Blocks.TEXT
    data: str


@dataclass
class Content:
    blocks: List[Block] = field(default_factory=list)


@dataclass
class Header:
    id: str = field(default_factory=identifier)
    timestamp: str = field(default_factory=timestamp)
    format: Block = field(default_factory=Blocks)
    reply_to: Optional[str] = None
    correlation_id: Optional[str] = None


@dataclass
class Message(Generic[T]):
    def __init__(self):
        self.payload = None
        self.headers = None

    blocks: List[Block]


@dataclass
class Footer:
    annotation: Optional[str] = None
    labels: Optional[List[str]] = field(default_factory=list)
    embedding: Optional[List[float]] = field(default_factory=list)


@dataclass
class Prompt(Model):
    name: str
    description: str
    labels: List[str]
    blocks: List[Block]


@dataclass
class Payload(Generic[T]):
    headers: Header
    message: Message
    footer: Optional[Footer] = None
    schema_version: str = "1.0"
