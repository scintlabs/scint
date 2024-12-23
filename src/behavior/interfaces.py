from enum import Enum

from src.base.models import OutputMessage
from ..base.protocols import Interface
from .types import ControllerType


class OutputFormat(Enum):
    Construct = OutputMessage
    Interpret = OutputMessage
    Process = OutputMessage
    Search = OutputMessage


class Controller(metaclass=ControllerType):
    def __init__(self, *args, **kwargs): ...

    async def construct(self): ...

    async def interpret(self): ...

    async def process(self): ...

    async def search(self): ...


__all__ = Interface
