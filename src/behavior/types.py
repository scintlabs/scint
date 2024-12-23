from ..base import Prototype


class ControllerType(Prototype):
    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)
