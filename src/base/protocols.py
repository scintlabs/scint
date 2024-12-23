from typing import Protocol as ProtocolType, runtime_checkable, Any

from ..base.models import Model


@runtime_checkable
class Interface(ProtocolType):
    async def input(self, input: Model): ...

    async def parse(self): ...

    async def output(self, output: Model): ...


@runtime_checkable
class Process(ProtocolType):
    async def start(self): ...

    async def stop(self): ...


@runtime_checkable
class Memory(ProtocolType):
    async def compose(self, input: Any = None): ...

    async def encode(self, obj: Any): ...

    async def ammend(self, input: Any = None): ...
