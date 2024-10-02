from scint.framework.types.base import BaseType


class Interface(metaclass=BaseType):
    def __init__(self, *args, **kwargs):
        for item in args:
            setattr(self, type(item).__name__, item)
        for key, value in kwargs.items():
            setattr(self, key, value)
