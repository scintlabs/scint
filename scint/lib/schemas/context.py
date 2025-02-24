from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Type

from redis.client import Redis

from scint.lib.prototypes.composer import Composable
from scint.lib.prototypes.scheduler import Observable
from scint.lib.schemas.signals import Prompt, Intention, Message, Response
from scint.lib.schemas.signals import ToolCall, Result
from scint.lib.schemas.tasks import Task
from scint.lib.types.model import Model
from scint.lib.types.struct import Struct
from scint.lib.types.tools import Tool
from scint.lib.types.traits import Trait


_context: Dict[str, Any] = {}
_redis = Redis(host="localhost", port=6379, db=0)


class ProcessContext(Model):
    task: Optional[Task] = None
    tasks: List[Task] = []
    results: List[Result] = []

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


class InterfaceContext(Model):
    messages: List[Message | Result | Response | ToolCall] = []

    def update(self, *args):
        for a in args:
            if isinstance(a, (Message, Result, Response, ToolCall)):
                self.messages.append(a)

    @property
    def model(self):
        messages = []
        for m in self.messages:
            messages.append(m.model)
        return {"messages": messages}


class ComposedContext(Model):
    intention: Optional[Intention] = None
    prompts: List[Prompt] = []


class Context(Struct):
    traits = (Composable, Observable)
    interface = InterfaceContext()
    prototype: Type
    tools: List[Tool]

    def update(self, *args):
        self.interface.update(*args)
        self._sync_to_redis()

    def _sync_to_redis(self) -> None:
        key = f"context:{self.prototype.prototype}"
        serialized = self.encode()
        _redis.set(key, serialized)

    def encode(self) -> bytes:
        data = {"interface": self.interface.model_dump()}
        data["interface"]["tools"] = [t.model for t in self.prototype._tools.values()]
        return json.dumps(data).encode("utf-8")

    @classmethod
    def decode(cls, data):
        data_dict = json.loads(data)
        context = cls()
        context.interface = InterfaceContext.model_validate(data_dict["interface"])
        return context

    @property
    def model(self):
        return {
            **self.interface.model,
            "tools": [t.model for t in self.prototype._tools.values()],
        }


class ContextProvider:
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
        if instance is not None and hasattr(instance, "prototype"):
            stored_data = _redis.get(f"context:{instance.prototype}")
            if not stored_data:
                context = Context()
                context.prototype = instance
                return context
            else:
                context = Context.decode(stored_data)
                context.prototype = instance
                return context

        all_keys = _redis.keys("context:*")
        result = {}
        for k in all_keys:
            k_str = k.decode("utf-8")
            data = _redis.get(k)
            if data:
                context_obj = Context.decode(data)
                instance_type = k_str.split("context:")[-1]
                context_obj.prototype = instance_type
                result[instance_type] = context_obj
                return result
        return self

    def __set__(self, instance: Any, value: Any) -> None:
        raise AttributeError("Context cannot be set directly")
