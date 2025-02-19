from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from scint.lib.schema.models import Model, Prompt
from scint.lib.schema.signals import Event, Intention, Message
from scint.lib.types.struct import Struct
from scint.lib.types.tasks import Task
from scint.lib.types.tools import Tool
from scint.lib.types.traits import Trait, Traits


EMBEDDING_THRESHOLD = 6
SIMILARITY_THRESHOLD = 0.8
SPLIT_MESSAGE_COUNT = 2


_context: Dict[str, ContextProvider] = {}


class Composable(Trait):
    def update(self, data: Any):
        pass

    def model(self):
        return {}


class ContextProvider:
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
        if instance is None:
            return self

        if instance.type != "Composer":
            if instance.id not in _context:
                _context[instance.id] = Context()
            return _context[instance.id]

        return _context

    def __set__(self, instance: Any, value: Any) -> None:
        raise AttributeError("Context cannot be set directly")


class TemporalContext(Model):
    traits: Traits = Traits(Composable)
    current: ActiveContext | SemanticContext = None
    prev: ActiveContext | SemanticContext = None
    next: ActiveContext | SemanticContext = None


class ActiveContext(Model):
    goal: Task = None
    events: List[Event] = []
    messages: List[Message] = []
    tasks: List[Task] = []
    tools: List[Tool] = []


class SemanticContext(Model):
    intention: Intention = None
    prompts: List[Prompt] = []
    messages: List[Message] = []
    tasks: List[Task] = []
    tools: List[Tool] = []


class Context(Struct):
    active: ActiveContext = ActiveContext()
    semantic: SemanticContext = SemanticContext()

    def update(self, *args):
        for a in args:
            match type(a).__name__:
                case "Message":
                    self.active.messages.append(a)
                case "Response":
                    self.active.messages.append(a)
                case "Event":
                    self.active.messages.append(a)
                case "Prompt":
                    self.semantic.prompts.append(a)
                case "Task":
                    self.tasks.append(a)
                case _:
                    pass

    @property
    def model(self):
        return {
            "messages": [*self.active.messages, *self.semantic.messages],
            "tools": [],
        }
