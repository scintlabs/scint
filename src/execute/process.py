from __future__ import annotations

from enum import Enum
from typing import Callable, List

from attr import field
from attrs import define

from src.base.actor import Actor
from src.base.protocol import agentic
from src.base.types import Format
from src.compose.composer import Outline
from src.base.records import Content


class ExecutionEvent(Enum):
    Execution = {"type": "function_call"}
    Result = {"type": "function_call_output"}


@define
class Result:
    outline_id: str = field(default=None)
    task_id: str = field(default=None)
    result: Result = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)


@agentic
class Process(Actor):
    outline: Outline = field(default=None)
    results: List[Result] = field(factory=list)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)
