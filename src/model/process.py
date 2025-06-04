from __future__ import annotations

from enum import Enum
from typing import Callable, List

from attrs import define, field

from src.runtime.protocol import agentic
from src.runtime.types import Format
from src.model.outline import Outline
from src.model.records import Content


class ExecutionEvent(Enum):
    Execution = {"type": "function_call"}
    Result = {"type": "function_call_output"}


@agentic
class Process:
    outline: Outline = field(default=None)
    results: List[Result] = field(factory=list)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)


@define
class Result:
    outline_id: str = field(default=None)
    task_id: str = field(default=None)
    result: Result = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)
