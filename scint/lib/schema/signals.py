from __future__ import annotations

from enum import Enum
from uuid import uuid4
from datetime import datetime as dt, timezone as tz
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from scint.lib.schema.records import Content


def parse_created(created_str: str) -> dt:
    return dt.fromisoformat(created_str)


def sort_signals_by_time(signals: List[Signal]) -> List[Signal]:
    return sorted(signals, key=lambda signal: parse_created(signal.created))


class Signal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: dt.now(tz.utc).isoformat())
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Channel(Signal): ...


class EventType(Enum):
    ToolCall = "ToolCall"
    ToolResult = "ToolResult"
    Query = "Query"


class ResultType(Enum):
    FunctionCall = "FunctionCall"
    ProcessCall = "ProcessCall"
    SearchQuery = "SearchQuery"


class DataEvent(Signal):
    catalog: str
    path: str
    operation: str
    content_id: str


class Event(Signal):
    type: EventType
    content: str


class Result(Signal):
    type: ResultType
    content: Result

    @property
    def model(self):
        {"role": "tool", "tool_call_id": self.call_id, "content": self.result}


class ProcessCall(Signal):
    call_id: str
    content: List[Result]

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.call_id,
            "results": [r.content for r in self.content],
        }


class FunctionCall(Signal):
    call_id: str
    result: Result

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.call_id,
            "content": self.result.content,
        }


class Response(Signal):
    content: List[Content]
    entities: Optional[List[str]]
    keywords: List[str]
    prediction: List[str]

    @property
    def model(self):
        return {"role": "assistant", "content": self.content}


class Message(Signal):
    content: str
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "user", "content": self.content}


MessageType = Message | Response | FunctionCall | ProcessCall | Result
