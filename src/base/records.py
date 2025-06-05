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
class Task:
    id: str = field(default=None)
    instructions: Instructions = field(default=None)


@define
class Outline:
    id: str = field(default=None)
    tasks: List[Task] = field(factory=list)
    instructions: Instructions = field(default=None)


@define
class TaskResult:
    task_id: str = field()
    content: Content = field()


@define
class ProcessResults:
    process_id: str = field()
    task_results: List[TaskResult] = field(factory=list)


@define
class Process:
    id: str = field(default=None)
    outlines: List[Outline] = field(factory=list)
    results: ProcessResults = field(default=None)


__all__ = Message, Instructions, Response, ToolCall, ToolResult
