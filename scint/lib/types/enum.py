from __future__ import annotations

from enum import Enum, EnumType
from typing import Any, Dict, Type, Tuple


class FactoryType(EnumType):
    def __call__(cls, *args, **kwargs):
        if (
            args
            and len(args) >= 3
            and isinstance(args[0], str)
            and isinstance(args[1], tuple)
            and isinstance(args[2], dict)
        ):
            return cls._make(*args, **kwargs)
        else:
            return super().__call__(*args, **kwargs)


class Factory(Enum, metaclass=FactoryType):
    def __init__(self, name: str, prototype: str, params=None, build=False):
        self.type_name = name
        self.prototype = prototype
        self.params = params
        self.build = self.__call__(name, prototype, params)

    def __call__(self, name: str, prototype, params):
        type = self._get_type(name, prototype, params)
        return type

    def _get_type(self, name: str, prototype, params):
        try:
            if prototype is not None:
                from importlib import import_module

                module = import_module(f"scint.lib.prototypes.{"interface"}")
                return getattr(module, name)

        except Exception as e:
            raise Exception(f"Couldn't create type '{name}': {e}.")

    @classmethod
    def _make(cls, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        member = next(iter(cls))
        return member.__call__(name, bases, dct)
