from __future__ import annotations

from typing import Callable, List

from attrs import define, field

from src.runtime.protocol import agentic
from src.model.records import Content, Directions, Result
from src.runtime.types import Format


@define
class Task:
    result: Result = field(default=None)
    directions: Directions = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)


@agentic
class Outline:
    tasks: List[Task] = field(factory=list)
    directions: Directions = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)
