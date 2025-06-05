from __future__ import annotations

from typing import Callable, List

from attrs import define, field

from .records import Content
from .outline import Outline
from src.core.agents.protocol import agentic
from src.core.types import Record


@agentic
class Process:
    outline: Outline = field(default=None)
    results: List[Result] = field(factory=list)

    @classmethod
    def create(cls, content: Content, format: Record, tools: List[Callable]):
        return cls(content, format, tools)


@define
class Result:
    outline_id: str = field(default=None)
    task_id: str = field(default=None)
    result: Result = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Record, tools: List[Callable]):
        return cls(content, format, tools)
