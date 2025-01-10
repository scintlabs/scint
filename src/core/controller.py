from __future__ import annotations

from enum import Enum
from types import new_class

from src.core.agents import Agentic
from src.core.types import BaseType
from src.memory import Composer, Mapper
from src.processes import Orchestrator


class Interface(Agentic, metaclass=BaseType):
    def __init__(self, context, /, process=None, mapping=None):
        self.context = context
        self.process = process
        self.mapping = mapping


class Controllers(str, Enum):
    composer = Composer()
    orchestrator = Orchestrator()
    mapper = Mapper()

    def load(self, name: str, *args, **kwargs):
        try:
            mapping = Mapper.get_mapping(name=self.value, kwargs=kwargs)
            return mapping()
        except Exception as e:
            raise RuntimeError(f"Error instantiating {self.value}: {str(e)}")


class Controller(Agentic, metaclass=BaseType):
    def __init__(self):
        self.composer = Composer()
        self.orchestrator = Orchestrator()
        self.mapper = Mapper()

    def load(self, name, *aspects, **kwargs):
        bases = aspects
        try:
            interface = self.create_interface(
                name=self.value, bases=bases, kwargs=kwargs
            )
            return interface()
        except Exception as e:
            raise RuntimeError(f"Error instantiating {self.value}: {str(e)}")

    def create_interface(self, name, /, bases, module, *args, **kwargs):
        dct = {"__module__": __name__ if module is None else module}
        dct.update(kwargs) if kwargs else None
        return new_class(name, (), {}, lambda ns: ns.update(dct))
