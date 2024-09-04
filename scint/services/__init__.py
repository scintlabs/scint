from scint.core import BaseType


class Service(metaclass=BaseType):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
