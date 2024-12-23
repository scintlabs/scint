from ..base.lib.language import get_completion, get_embedding
from ..base import Prototype


class SwitchType(Prototype):
    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


class StructType(Prototype):
    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


__all__ = get_completion, get_embedding
