from __future__ import annotations

from typing import Callable, List

from attrs import define, field

from src.base.actor import Actor
from src.base.protocol import agentic
from src.base.records import Content, Directions, Result
from src.base.types import Format


@define
class Task:
    directions: Directions = field()
    result: Result = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)


@agentic
class Outline(Actor):
    tasks: List[Task] = field(factory=list)
    directions: Directions = field(default=None)

    @classmethod
    def create(cls, content: Content, format: Format, tools: List[Callable]):
        return cls(content, format, tools)
