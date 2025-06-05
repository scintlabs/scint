from __future__ import annotations

from typing import Any, Dict, List, TypeAlias, Union, TypeVar

from attrs import define, field

T = TypeVar("T")
Content: TypeAlias = Union[str, List[str], Dict[str, Any]]


@define
class Message:
    content: Content = field(default=None)


@define
class Response:
    content = field(factory=list)


@define
class Instructions:
    name = field(default=None)
    content = field(default=None)
    category = field(default=None)


@define
class ToolCall:
    call_id: str = field(default=None)
    tool_name: str = field(factory=str)
    arguments: Dict[str, Any] = field(factory=dict)


@define
class ToolResult:
    call_id = field(default=None)
    tool_name: str = field(factory=str)
    content: Content = field(factory=str)


@define
class Metadata:
    name: str = field(default=None)
    description: str = field(default=None)
    recap: str = field(default=None)
    annotations: List[str] = field(factory=list)
    embedding: List[float] = field(factory=list, repr=False)
    keywords: List[str] = field(factory=list)
    events: List[Dict[str, Any]] = field(factory=list)


__all__ = Message, Metadata, Instructions, Response, ToolCall, ToolResult
