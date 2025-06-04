from __future__ import annotations

from enum import Enum
from importlib import import_module
from typing import TypeAlias, Union

from .context import Context
from .outline import Outline
from .process import Process
from .records import Content, Message, Metadata

Model: TypeAlias = Union[Context, Outline, Process, Content]


class OutputFormat(Enum):
    Activity = ("Activity", None)
    Instruction = ("Instruction", None)
    Message = ("Message", None)
    Metadata = ("Metadata", None)
    Task = ("Activity", None)
    Query = ("Query", None)

    def __init__(self, format, func):
        self.format = format
        self.func = func

    def __call__(self):
        mod = import_module("src.model.records")
        cls = getattr(mod, self.format)
        return cls


__all__ = Context, Outline, Process, Content, Model, Metadata, Message
