from __future__ import annotations

import asyncio
from enum import Enum

from typing import Any, Dict, List, Optional, TypeAlias, Union, TypeVar

from attrs import define, field
from meilisearch_python_sdk.models.search import Hybrid

from src.base.utils import timestamp

T = TypeVar("T")
Content: TypeAlias = Union[str, List[str], Dict[str, Any]]


@define
class Metadata:
    name: str = field(default=None)
    description: str = field(default=None)
    recap: str = field(default=None)
    annotations: List[str] = field(factory=list)
    embedding: List[float] = field(factory=list, repr=False)
    keywords: List[str] = field(factory=list)
    events: List[Event] = field(factory=list)


@define
class Message:
    content: Content = field(default=None)
    metadata: Metadata = field(default=None)

    @classmethod
    def create(cls, content: str):
        return cls(content=content, metadata=Metadata())


def Command(name: str, **kwargs):
    return Message(f"cmd:{name}", kwargs)


def Event(name: str, **kwargs):
    return Message(f"evt:{name}", kwargs)


def Query(name: str, **kwargs):
    return Message(f"qry:{name}", kwargs)


class ExecutionEvent(Enum):
    Execution = {"type": "function_call"}
    Result = {"type": "function_call_output"}


class ThreadEvent(Enum):
    Created = {"created": lambda: timestamp()}
    Staled = {"staled": lambda: timestamp()}
    Encoded = {"encoded": lambda: timestamp()}
    Purged = {"purged": lambda: timestamp()}

    def __init__(self, event):
        self.event = event

    def __call__(self, content: str = None):
        if content is not None:
            self.event["content"] = content
        return self.event


@define
class Instructions:
    name = field(default=None)
    content = field(default=None)
    category = field(default=None)


@define
class Directions:
    content = field(default=None)


@define
class Response:
    content = field(factory=list)
    metadata: Metadata = field(default=Metadata())


@define
class Execution:
    call_id: str = field(default=None)
    tool_name: str = field(factory=str)
    arguments: Dict[str, Any] = field(factory=dict)


@define
class Result:
    call_id = field(default=None)
    tool_name: str = field(factory=str)
    content: Content = field(factory=str)


@define
class Search:
    query = field(default=None)
    filter = field(type=Optional[str], default=None)
    hybrid = field(
        type=Optional[Hybrid], default=Hybrid(semantic_ratio=0.9, embedder="default")
    )
    vector = field(type=Optional[List[float]], default=None)
    limit = field(type=Optional[int], default=6)


@define
class SearchHits:
    hits: List[Any] = field(factory=list)


Content: TypeAlias = Union[Message, Result, Search]
EncodedContent: TypeAlias = Union[Message, Result, Search]
