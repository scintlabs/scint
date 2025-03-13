from typing import List

from src.types.agents import Function, Output, Prompt
from src.types.typing import _finalize_type


class AspectType(type):
    def __new__(cls, name, bases, dct):
        def __init__(self, context, /, *args):
            self.context = context
            for t in self.traits:
                t.init(self)

        dct["__init__"] = __init__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Aspect(metaclass=AspectType):
    prompts: List[Prompt] = []
    output: Output
    functions: List[Function] = []

    async def evaluate(self):
        res = await self.parse()
        self.context.update(res)
        return res
