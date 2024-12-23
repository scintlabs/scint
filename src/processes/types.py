from typing import List
from typing import Protocol as ProtocolType, runtime_checkable

from ..base.types import Prototype
from ..base.models import Memory


@runtime_checkable
class Process(ProtocolType):
    async def start(self): ...

    async def stop(self): ...


class ProcessorType(Prototype):
    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


class Processor(Process, metaclass=ProcessorType):
    def __init__(self, *args, **kwargs):
        self._contexts: List[Memory] = []
