from __future__ import annotations

from enum import Enum, auto
from types import new_class
from typing import Any, Generic, TypeVar

from src.core.types import BaseType, Struct
from src.core.agents import Agentic


T = TypeVar("T")


class Mapping(Struct):
    structs: Any[Struct]


class Mappings(str, Enum):
    CONFIG = auto()
    INDEX = auto()
    GRAPH = auto()
    TREE = auto()


class Mapper(Agentic, metaclass=BaseType):
    def __init__(self): ...

    def get_mapping(self, name: str, /, module: str = None, **kwargs):
        pass

    def create_mapping(self, name: str, /, module: str = None, **kwargs) -> Generic[T]:
        dct = {"__module__": __name__ if module is None else module}
        dct.update(kwargs) if kwargs else None
        return new_class(name, (), {}, lambda ns: ns.update(dct))

    def update_mapping(self, name: str, data: dict):
        pass

    def load_mapping(self, name: str, params: dict):
        pass

    def save_mapping(self):
        pass

    @property
    def model(self):
        return {
            "events": [],
            "functions": [],
        }
