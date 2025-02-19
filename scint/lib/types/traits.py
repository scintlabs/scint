from __future__ import annotations

from types import MethodType, FunctionType

from scint.lib.types.typing import _finalize_type


class TraitType(type):
    def __new__(cls, name, bases, dct):
        @staticmethod
        def __init_trait__(other):
            for k, v in dct.items():
                if not k.startswith("_") and isinstance(v, (FunctionType, MethodType)):
                    print(f"Adding {k} to {other}")
                    setattr(other, k, MethodType(v, other))

        dct["type"] = "Trait"
        dct["__init_trait__"] = __init_trait__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Trait(metaclass=TraitType):
    def __init__(self): ...


def Traits(other, *traits):
    for t in traits:
        t.__init_trait__(other)
        return other
