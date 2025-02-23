from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Type

from redis.client import Redis

from scint.lib.prototypes.notifier import Observable, Observe
from scint.lib.schemas.models import Model
from scint.lib.schemas.signals import (
    Intention,
    Message,
    Prompt,
    Response,
    Result,
    ToolCall,
)
from scint.lib.schemas.tasks import Task
from scint.lib.types.struct import Struct
from scint.lib.types.tools import Tool
from scint.lib.types.traits import Trait


_context: Dict[str, Any] = {}
_redis = Redis(host="localhost", port=6379, db=0)


class ContextConnector:
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
        if instance is None:
            return self

        key = f"context:{instance.type}"
        if instance.type != Composer:
            stored_data = _redis.get(key)
            if not stored_data:
                c = Context(other=instance.type)
                _redis.set(key, c.encode)
                return c
            else:
                return Context.decode(stored_data)

        all_keys = _redis.keys("context:*")
        result = {}
        for k in all_keys:
            k_str = k.decode("utf-8")
            data = _redis.get(k_str)
            if data:
                context_obj = Context.decode(data)
                instance_type = k_str.split("context:")[-1]
                result[instance_type] = context_obj
        return result

    def __set__(self, instance: Any, value: Any) -> None:
        raise AttributeError("Context cannot be set directly")


class SemanticContext(Model):
    intention: Optional[Intention] = None
    prompts: List[Prompt] = []

    def update(self, *args):
        for a in args:
            if isinstance(a, (Message, Result, Response, ToolCall)):
                self.messages.append(a)

    @property
    def model(self):
        messages = []
        if self.intention is not None:
            messages.append(self.intention.model)

        for p in self.prompts:
            messages.append(p.model)

        return {"messages": messages}


class BaseContext(Model):
    messages: List[Message] = []
    tools: List[Tool] = []

    def update(self, *args):
        for a in args:
            if isinstance(a, (Message, Result, Response, ToolCall)):
                self.messages.append(a)

    @property
    def model(self):
        messages = []
        for m in self.messages:
            messages.append(m.model)

        return {
            "messages": messages,
            "tools": [t.model for t in self.tools],
        }


class ProcessContext(Model):
    task: Optional[Task] = None
    tasks: List[Task] = []
    results: List[Result] = []
    tools: List[Tool] = []

    def update(self, *args):
        for a in args:
            match type(a).__name__:
                case "Task":
                    self.tasks.append(a)
                case "Result":
                    self.results.append(a)
                case _:
                    pass

    @property
    def model(self):
        return {"tools": []}


class Context(Struct, traits=(Observable,), other=None):
    other: str = None
    base: BaseContext = BaseContext()
    process: ProcessContext = ProcessContext()
    semantic: SemanticContext = SemanticContext()

    def __init__(self, other):
        self.other = other

    def update(self, other, *args):
        if self.other is None:
            self.other = other
        self.base.update(*args)
        self.process.update(*args)
        self.save()

    def load(self):
        if not self.other:
            raise ValueError(f"Context {self.other} is not set; cannot load context.")
        data = _redis.get(f"context:{self.other}")
        raw = json.loads(data)
        self.process = BaseContext(**raw.get("process", {}))
        self.base = BaseContext(**raw.get("base", {}))

    def save(self):
        if not self.other:
            raise ValueError(
                f"Context {self.other} is not set; cannot build a proper key."
            )
        data = self.encode
        _redis.set(f"context:{self.other}", data)

    @property
    def encode(self):
        data = self.base.model_dump()
        return json.dumps(data)

    @classmethod
    def decode(cls, data: str):
        raw = json.loads(data)
        return cls(
            base=BaseContext(**raw.get("base", {})),
            process=ProcessContext(**raw.get("process", {})),
        )

    @property
    def model(self):
        return {
            **self.semantic.model,
            **self.process.model,
            **self.base.model,
        }


class Compose(Trait):
    def compose(self):
        pass

    def search_intentions(self, message: Message):
        return None

    def search_messages(self, message: Message):
        return None

    def search_tools(self, message: Message):
        return None

    def search_tasks(self, message: Message):
        return None


class Composer(Struct, traits=(Compose, Observe)): ...


# class ContextConnector:
#     def __set_name__(self, owner: Type[Any], name: str) -> None:
#         self.name = name

#     def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
#         if instance is None:
#             return self

#         if instance.id != "Composer":
#             if instance.id not in _context:
#                 _context[instance.id] = Context()
#             return _context[instance.id]
#         return _context

#     def __set__(self, instance: Any, value: Any) -> None:
#         raise AttributeError("Context cannot be set directly")
