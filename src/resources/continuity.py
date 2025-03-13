from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from redis.client import Redis


from src.schemas.resources import Provider
from src.types.agents import Prompt
from src.types.models import Model, Message


state_provider = Provider(
    name="Redis",
    module=Redis,
    parameters={"host": "localhost", "port": 6379, "db": 0},
)


class Context(Model):
    identity: str
    prompts: List[Prompt] = []
    interfaces: List[Any] = []
    constructs: List[Any] = []
    messages: List[Message] = []
    scratch: Optional[Any] = None

    def update(self, *args):
        for a in args:
            match a:
                case Prompt():
                    self.prompts = [a]
                case True if type(a).endswith("Message"):
                    self.messages = [a]
                case "Trait" if type(a).__name__:
                    self.traits = [a]
                    self.__init_traits__(self.traits)
                case "Interface" if type(a).__name__:
                    self.interfaces = [a.model]
                case "Frame" if type(a).__name__:
                    self.frames = [a]
                case object() if hasattr(a, "frames"):
                    self.frames = a.frames

    def add(self, *args):
        for a in args:
            match a:
                case Prompt():
                    self.prompts.append(a)
                case True if type(a).endswith("Message"):
                    self.messages.append(a)
                case "Trait" if type(a).__name__:
                    self.traits.append(a.name)
                    self.__init_traits__(a)
                case "Interface" if type(a).__name__:
                    self.interfaces = [a.model]
                case "Frame" if type(a).__name__:
                    self.frames = [a]
                case object() if hasattr(a, "frames"):
                    self.frames = a.frames

    @property
    def build_model(self):
        messages = []
        for m in self.prompts:
            messages.append(m.model)
        return {"messages": messages, "tools": self.interfaces}


class State(Model):
    identity: str
    prompts: List[Prompt] = []
    traits: List[Any] = []
    frames: List[Any] = []
    processes: List[Any] = []
    interfaces: List[Any] = []
    scratch: Optional[Any] = None

    def update(self, *args):
        for a in args:
            match a:
                case Prompt():
                    self.prompts = [a]
                case True if type(a).endswith("Message"):
                    self.messages = [a]
                case "Trait" if type(a).__name__:
                    self.traits = [a]
                    self.__init_traits__(self.traits)
                case "Interface" if type(a).__name__:
                    self.interfaces = [a.model]
                case "Frame" if type(a).__name__:
                    self.frames = [a]
                case object() if hasattr(a, "frames"):
                    self.frames = a.frames

    def add(self, *args):
        for a in args:
            match a:
                case Prompt():
                    self.prompts.append(a)
                case True if type(a).endswith("Message"):
                    self.messages.append(a)
                case "Trait" if type(a).__name__:
                    self.traits.append(a.name)
                    self.__init_traits__(a)
                case "Interface" if type(a).__name__:
                    self.interfaces = [a.model]
                case "Frame" if type(a).__name__:
                    self.frames = [a]
                case object() if hasattr(a, "frames"):
                    self.frames = a.frames

    @property
    def build_model(self):
        messages = []
        for m in self.prompts:
            messages.append(m.model)
        return {"messages": messages, "tools": self.interfaces}


class DataModel:
    def __init__(self, base_model: Model):
        self.base_model = base_model
        self.instances: Dict[int, Model] = {}

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is not None:
            identity = instance.identity
            if identity not in self.instances:
                self.instances[identity] = self.base_model(identity)
            return self.instances[identity]

    def __set__(self, instance, value):

        self.instances[id(instance)] = value


class Continuity:
    def __init__(self, data_model, *args):
        self.data_model = data_model
        self.provider = state_provider.client()

    def __set_name__(self, owner, name):
        self.name = name

    def create(self, identity: str):
        obj = self.data_model(identity=identity)
        data = obj.model_dump()
        string = json.dumps(data)
        self.update(identity, string)
        return string

    def fetch(self, identity: str):
        res = self.provider.get(identity)
        return res if res is not None else self.create(identity)

    def update(self, identity: str, **kwargs):
        obj = self.fetch(identity)
        dct = json.loads(obj)

        try:
            for k, v in kwargs.items():
                if hasattr(dct, k):
                    setattr(dct, k, v)
            mdl = self.data_model.model_validate(**kwargs)
            self.provider.set(identity, mdl.model_dump_json())
        except Exception:
            raise
        return obj
