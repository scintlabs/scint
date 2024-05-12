import functools
from scint.base.modules.components.function import FuncType


async def argument():
    pass


def function_factory(argument):

    class Func(metaclass=FuncType):
        name = argument.__name__
        function = argument

        def __init__(self):
            self.name = self.name
            self.function = self.function

        def call(function):
            @functools.wraps(function)
            async def decorated(*args, **kwargs):
                function_instance = function(*args, **kwargs)
                async for result in function_instance(*args, **kwargs):
                    yield result

                yield decorated

    func = Func()
    return func
