from __future__ import annotations

from uuid import uuid4
from types import FunctionType
from typing import List, TypeAlias, Union

from attrs import field

from src.core.types.signals import Input, Output
from src.core.types.structure import Struct
from src.core.types.identity import activity


@activity
class Task:
    input: Input = field(default=None)
    tools: List[FunctionType] = field(factory=list)


@activity
class Analysis:
    task: Task = field(default=None)
    steps: List[Task] = field(factory=list)
    visited: List[Struct] = field(factory=list)
    tools: List[FunctionType] = field(factory=List)


@activity
class Composition:
    id: str = field(factory=lambda: str(uuid4()))
    task: Task = field(default=None)
    steps: List[Task] = field(factory=list)
    created: List[Struct] = field(factory=list)
    tools: List[FunctionType] = field(factory=List)


@activity
class Dialogue:
    id: str = field(factory=lambda: str(uuid4()))
    input: List[Input] = field(factory=list)
    output: List[Output] = field(factory=list)
    tools: List[FunctionType] = field(factory=List)


@activity
class Execution:
    id: str = field(factory=lambda: str(uuid4()))
    task: Task = field(default=None)
    steps: List[Task] = field(factory=list)
    visited: List[Struct] = field(factory=list)
    tools: List[FunctionType] = field(factory=List)


@activity
class Hypothesis:
    id: str = field(factory=lambda: str(uuid4()))
    task: Task = field(default=None)
    steps: List[Task] = field(factory=list)
    tools: List[FunctionType] = field(factory=List)


Activity: TypeAlias = Union[Analysis, Composition, Execution, Hypothesis]
