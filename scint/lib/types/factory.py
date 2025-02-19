from __future__ import annotations

from enum import Enum, EnumType
from types import new_class
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
    def __init__(self, name=False, bases=False, dct=False, new=False):
        self.type_name = name
        self.base = bases
        self.dct = dct
        self.new = self.__call__(name, bases, dct)

    def __call__(self, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        dct = self._get_type(name, bases, dct)
        return new_class(name, bases, {}, lambda ns: dct)

    def _get_type(self, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        from importlib import import_module

        try:
            match name:
                case "Entity":
                    module = import_module("scint.lib.entities", "Handler")
                    return getattr(module, name)
                case "Context":
                    module = import_module("scint.lib.context", "Context")
                    return getattr(module, name)
                case "Tool":
                    module = import_module("scint.lib.types.tools", "Tools")
                    return getattr(module, name)
        except Exception as e:
            raise Exception(f"Couldn't create type '{name}': {e}.")

    @classmethod
    def _make(cls, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        member = next(iter(cls))
        return member.__call__(name, bases, dct)
