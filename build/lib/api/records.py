from __future__ import annotations

from enum import Enum
from datetime import datetime
from typing import Dict, Generic, List, Optional, Any, TypeVar

from scint.lib.models.base import Record

P = TypeVar("P")


class BlockType(str, Enum):
    TEXT = "text"
    CODE = "code"
    FILE = "file"
    IMAGE = "image"


class Block(Record):
    data: str
    type: BlockType = BlockType.TEXT


class Event(Record):
    data: str
    origin: str
    created: str

    def __init__(self):
        self.created = self.timestamp()

    def timestamp(unix_ts=None):
        if unix_ts is None:
            return int(datetime.now().timestamp())
        else:
            try:
                return datetime.fromtimestamp(unix_ts).strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return "Invalid timestamp provided"


class Prompt(Record):
    name: str
    labels: List[str]
    content: List[Block]
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "system", "content": "".join([b.data for b in self.content])}


class Message(Record):
    content: List[Block] = []
    embedding: List[float] = []

    @property
    def model(self):
        return {"role": "user", "content": "".join([b.data for b in self.content])}


class Response(Record):
    annotation: str
    labels: List[str]
    content: List[Block]

    @property
    def model(self):
        return {"role": "assistant", "content": self.annotation}


class Instruction(Record):
    name: str
    labels: List[str]
    content: List[Block]
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "system", "content": "".join([b.data for b in self.content])}


class Task(Record):
    name: str
    content: List[Block] = []
    labels: List[str] = []


class Action(Record):
    id: str
    tool: str
    arguments: Dict[str, Any] = {}

    @property
    def model(self):
        return {"role": "function"}


class Result(Record):
    id: str = None
    content: List[Block]

    @property
    def model(self):
        return {"role": "tool", "tool_call_id": self.id, "content": self.content}


class Intention(Record):
    name: str
    labels: List[str]
    content: List[Block]
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "system", "content": "".join([b.data for b in self.content])}


class Argument(Record):
    name: str
    type: str
    value: Optional[Any] = None
    required: bool = False
    description: str = ""

    @property
    def model(self):
        return self.value if self.value else None


class Arguments(Record):
    args: List[Argument] = []
    kwargs: Dict[str, Argument] = {}

    @classmethod
    def create(cls, parser: Generic[P], build: bool = False):
        pass

    def merge(self, other: Arguments):
        self.args.extend(other.args)
        self.kwargs.update(other.kwargs)
        return self

    @property
    def model(self) -> Dict[str, Any]:
        return [*self.args, {k: v for k, v in self.kwargs.items()}]


class Index(Record):
    name: str
    key: str = "id"
    sortables: List[str] = []
    filterables: List[str] = []
    searchables: List[str] = []
