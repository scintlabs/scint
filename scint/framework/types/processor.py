from scint.framework.state.metadata import collector
from scint.framework.state.state import State
from scint.framework.types.base import BaseType


class ProcessorType(BaseType):
    def __new__(cls, name, bases, dct, **kwds):
        dct["_call_stack"] = []
        for key, value in dct.items():
            if callable(value) and not key.startswith("__"):
                if callable(value):
                    dct[key] = collector(value)
                elif not isinstance(value, State):
                    dct[key] = State()
        return super().__new__(cls, name, bases, dct)


class Processor(metaclass=ProcessorType):
    def __init__(self, context, *args, **kwargs):
        self.name = self.__name__
        self.context = context

        for item in args:
            setattr(self, type(item).__name__.lower(), item)
        for key, value in kwargs.items():
            setattr(self, key, value)
