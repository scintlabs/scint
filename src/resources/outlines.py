from __future__ import annotations

from typing import Callable, List

from attrs import define, field

from src.base.records import Content, Instructions


@define
class Task:
    id: str = field(default=None)
    result: Result = field(default=None)
    tasks: List[Task] = field(factory=list)
    instructions: Instructions = field(default=None)

    @classmethod
    def create(cls, content: Content, tools: List[Callable]):
        return cls(content, format, tools)


@define
class Result:
    outline_id: str = field(default=None)
    task_id: str = field(default=None)
    result: Result = field(default=None)

    @classmethod
    def create(cls, content: Content, tools: List[Callable]):
        return cls(content, format, tools)


@define
class Outline:
    tasks: List[Task] = field(factory=list)
    instructions: Instructions = field(default=None)

    @classmethod
    def create(cls, content: Content, tools: List[Callable]):
        return cls(content, format, tools)


@define
class Outlines:
    outlines: List[Outline] = field(factory=list)
    instructions: Instructions = field(default=None)

    @classmethod
    def create(cls, content: Content, tools: List[Callable]):
        return cls(content, format, tools)
