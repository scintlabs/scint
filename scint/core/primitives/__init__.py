from scint.core import BaseType


class Primitive(metaclass=BaseType):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
