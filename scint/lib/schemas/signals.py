from __future__ import annotations

from enum import Enum
import json
from uuid import uuid4
from datetime import datetime as dt, timezone as tz
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


def parse_created(created_str: str) -> dt:
    return dt.fromisoformat(created_str)


def sort_signals_by_time(signals: List[Signal]) -> List[Signal]:
    return sorted(signals, key=lambda signal: parse_created(signal.timestamp))


class Signal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: str(dt.now(tz.utc).isoformat()))
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())


class BlockType(Enum):
    TextBlock = "TextBlock"
    CodeBlock = "CodeBlock"
    ImageBlock = "ImageBlock"
    AudioBlock = "AudioBlock"
    VideoBlock = "VideoBlock"
    BinaryBlock = "BinaryBlock"


class Block(Signal):
    content: str
    annotation: Optional[str] = None


class EventType(Enum):
    ToolCall = "ToolCall"
    ToolResult = "ToolResult"
    Query = "Query"


class Event(Signal):
    type: EventType
    content: str


class Prompt(Signal):
    name: str
    content: str

    @classmethod
    def from_docstring(cls, docstring: str):
        lines = docstring.strip().split("\n")
        name = lines[0].strip()
        content_start = 3
        content = "\n".join(lines[content_start:]).strip()
        return cls(name=name, content=content)

    @property
    def model(self):
        return {
            "role": "system",
            "content": f"{self.name}\n{self.content}]",
        }


class Intention(Signal):
    blocks: List[Block]
    entities: Optional[List[str]]
    keywords: List[str]
    prediction: List[str]
    annotation: str

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": f"{self.timestamp}\n".join(b.content for b in self.blocks),
        }


class ToolCall(Signal):
    tool_call_id: str
    name: str
    arguments: Dict[str, Any]

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": self.tool_call_id,
                    "type": "function",
                    "function": {
                        "name": self.name,
                        "arguments": json.dumps(self.arguments),
                    },
                }
            ],
        }


class Result(Signal):
    tool_call_id: Optional[str] = None
    blocks: List[Block]

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "content": f"{self.timestamp}\n".join(b.content for b in self.blocks),
        }


class Message(Signal):
    content: str
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "user", "content": f"{self.timestamp}\n{self.content}"}


class Response(Signal):
    blocks: List[Block]
    keywords: List[str]
    prediction: List[str]
    annotation: str

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": f"{self.timestamp}\n".join(b.content for b in self.blocks),
        }


MessageType = Message | Response | ToolCall | Result
