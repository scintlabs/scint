from __future__ import annotations
from typing import List

from src.types.traits import Trait
from src.types.typing import _finalize_type


class StructType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        new_bases = [b for b in bases if not isinstance(b, Trait)]
        traits = [b for b in bases if isinstance(b, Trait)]
        return super().__prepare__(name, tuple(new_bases), {"traits": traits})

    def __new__(cls, name, bases, dct, **kwds):
        def __init__(self, *args, **kwargs):
            traits = kwds.get("traits", [])

            for a in args:
                if isinstance(a, Trait):
                    traits.append(a)
            self.__init_traits__(traits)

        def __init_traits__(self, traits: List[Trait] = None):
            self._traits = [*traits]
            for t in self._traits:
                other = self
                t.__init_trait__(other)

        dct["traits"] = __init_traits__
        dct["__init__"] = __init__
        dct["__init_traits__"] = __init_traits__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Struct(metaclass=StructType): ...
