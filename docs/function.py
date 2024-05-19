import functools
import inspect

from scint.support.types import Function, FunctionParams
from scint.controllers.intelligence import IntelligenceController


def function_factory(argument):
    """
    """
    class Func(metaclass=FuncType):
        """
        """
        name = argument.__name__
        function = argument

        def __init__(self):
            self.name = self.name
            self.function = self.function

        def call(self, function):
            """
            """
            @functools.wraps(function)
            async def decorated(*args, **kwargs):
                """
                """
                function_instance = self.function.call(*args, **kwargs)
                async for result in function_instance(*args, **kwargs):
                    yield result

                yield decorated

    func = Func()
    return func


class FuncType(type):
    """
    """
    description = None
    props = {}
    function = None
    intelligence = IntelligenceController()

    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return {}

    def __new__(cls, name, bases, dct, **kwds):
        super().__new__(cls, name, bases, dct, **kwds)
        function = dct.get("function")
        description = dct.get("description")
        props = dct.get("props")
        name = function.name
        signature = inspect.signature(function)
        required = [
            param_name
            for param_name, param in signature.parameters.items()
            if param.default == inspect.Parameter.empty and param_name != "self"
        ]

        dct["intelligence"] = cls.intelligence
        dct["name"] = name
        dct["required"] = required
        dct["metadata"] = Function(
            type="function",
            name=name,
            description=description,
            parameters=FunctionParams(
                type="object",
                properties=props,
                required=required,
            ),
        )

        return type.__new__(cls, name, bases, dct, **kwds)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Function(metaclass=FuncType):
    pass

    async def call(self, *args, **kwargs):
        """
        """
        raise NotImplementedError
