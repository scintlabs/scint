from .types import SwitchType, StructType
from ..base import Model, Interface, Memory
from ..base.lib.language import get_completion


class Struct(Interface, metaclass=StructType):
    def __init__(self, *args, **kwargs):
        self.context = Memory()

    async def input(self, input: Model):
        self.context.update(input)
        return await self.parse()

    async def parse(self):
        parsed = await get_completion(self.context)
        return await self.output(parsed)

    async def output(self, output: Model):
        self.context.update(output)
        return output


class Switch(metaclass=SwitchType):
    def __init__(self, *args, **kwargs):
        self.table = Struct()


__all__ = Switch, Struct
