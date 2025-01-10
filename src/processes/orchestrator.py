from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, TypeVar
from types import new_class
from typing_extensions import Generic

from src.core.agents import Agentic
from src.core.types import BaseType
from src.models.messages import Prompt


T = TypeVar("T")


class Orchestrator(Agentic, metaclass=BaseType):
    def __init__(self):
        self.instructions: List[Prompt] = []
        self.functions: List[Any] = []
        self.processes: Dict[str, Any] = {}

    def add_process(self, process): ...

    def create_process(self, name: str, /, module: str = None, **kwargs) -> Generic[T]:
        dct = {"__module__": __name__ if module is None else module}
        dct.update(kwargs) if kwargs else None
        return new_class(name, (), {}, lambda ns: ns.update(dct))


class Processes(str, Enum):
    Sequence = "Sequence"
    Worfklow = "Workflow"
    Parser = "Parser"

    def load(self, *args, **kwargs):
        try:
            process = Orchestrator.get_processor(name=self.value, kwargs=kwargs)
            return process()
        except Exception as e:
            raise RuntimeError(f"Error instantiating {self.value}: {str(e)}")
