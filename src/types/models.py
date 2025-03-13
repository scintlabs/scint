from __future__ import annotations

import json
from uuid import uuid4
from enum import Enum
from datetime import datetime as dt, timezone as tz
from typing import Any, List, Optional, Dict, Union

from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    created: str = Field(default_factory=lambda: str(dt.now(tz.utc).isoformat()))

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())

    @property
    def model(self):
        return self.model_dump()

    @property
    def schema(self):
        return self.model


class BlockType(str, Enum):
    TextBlock = "TextBlock"
    CodeBlock = "CodeBlock"
    ImageBlock = "ImageBlock"
    BinaryBlock = "BinaryBlock"


class Block(Model):
    content: str
    type: BlockType = BlockType.TextBlock

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())


class FileType(Enum):
    file = "file"
    directory = "directory"


class File(Model):
    name: str
    type: FileType


class Directory(Model):
    contents: List[Union[File, Directory]]
    name: str
    type: FileType


class Scaffold(Model):
    scaffold: List[Union[File, Directory]]


class Context(Model):
    messages: List[Message] = []
    scratch: Optional[Any] = None

    def update(self, *args):
        for a in args:
            self.messages.append(a)

    @property
    def model(self):
        return {"messages": [m.model for m in self.messages]}


class SignalType(str, Enum):
    Event = "Event"
    Message = "Message"
    Notification = "Notification"


class Signal(Model):
    id: str = Field(default_factory=lambda: str(uuid4()))

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())


class UserMessage(Signal):
    content: str
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "user", "content": f"{self.timestamp}\n{self.content}"}


class AgentMessage(Signal):
    content: List[Block]
    keywords: List[str]
    prediction: List[str]
    annotation: str

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": f"{self.timestamp}\n".join(b.content for b in self.content),
        }


class QueryMessage(Signal):
    index_name: str
    input: str
    category: Optional[str] = None
    limit: int = 4


class FunctionCall(Signal):
    call_id: str
    name: str
    arguments: Dict[str, Any]

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": self.call_id,
                    "type": "function",
                    "function": {
                        "name": self.name,
                        "arguments": json.dumps(self.arguments),
                    },
                }
            ],
        }


class FunctionResult(Signal):
    call_id: Optional[str] = None
    content: Optional[str] = None

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.call_id,
            "content": f"{self.timestamp}\n{self.content}",
        }


Message = Union[UserMessage, AgentMessage, FunctionCall, FunctionResult]
