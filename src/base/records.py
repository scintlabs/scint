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


__all__ = Message, Instructions, Response, ToolCall, ToolResult
