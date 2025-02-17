from __future__ import annotations

from typing_extensions import TypeVar
from uuid import uuid4
from types import FunctionType, MethodType
from typing import Callable, Dict, Any, Generator, List, Union

import numpy as np
from pydantic import BaseModel, ConfigDict


class BaseType(type):
    def __new__(cls, name, bases, dct, **kwds):
        dct["id"] = str(uuid4())
        dct["name"] = name

        if any(hasattr(b, "_functions") for b in bases):
            functions = {}
            for k, v in dct.items():
                if callable(v) and not k.startswith("_"):
                    func = v
                    func.trait = k
                    functions[k] = func
            dct["_functions"] = functions
            # new = {k: v for k, v in dct.items() if k not in functions}
            # dct = new

        if any(hasattr(b, "id") for b in bases):
            dct["__init_subclass__"] = lambda *args, **kwargs: None
            dct["__subclasscheck__"] = lambda *args: False
        return super().__new__(cls, name, bases, dct, **kwds)


class Record(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Tool(metaclass=BaseType):
    name: str
    description: str
    parameters: Parameters
    function: Callable
    __slots__ = ()

    async def _(self, action: Action) -> Result:
        if action.name == self.name:
            return await self.function(**action.arguments)

    @property
    def serialize(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters.model,
                "strict": True,
            },
        }


class Trait(metaclass=BaseType):
    _functions: Dict[str, FunctionType] = {}
    __slots__ = ()


class Struct(metaclass=BaseType):
    _data: Dict[str, Any] = {}
    _traits: List[Trait] = []
    _origin: Struct = None
    _children: List[Struct] = []
    __slots__ = ()

    def __init__(self, objects=None, behaviors=None):
        if objects is not None:
            self.update(objects)
        if behaviors is not None:
            self.implement(behaviors)

    def implement(self, trait: Trait):
        for k, v in trait._functions.items():
            setattr(self, k, MethodType(v, self))
        self._traits.append(trait)

    def scrub(self, trait: Trait):
        for k, v in self.__dict__.items():
            if callable(v) and getattr(v, "trait") is trait.name:
                delattr(self, k)
        delattr(self._traits, trait.name)

    def connect(self):
        return self._children

    def share(self):
        return self.metadata

    def accept(self, aspect: Aspect):
        return aspect.join(self)

    @property
    def metadata(self):
        embeddings = []
        labels = set()
        weights = []

        for c in self._children:
            if c.embeddings is not None:
                embeddings.append(c.embeddings)
                weights.append(1)
            labels.update(c.labels)

        for v in self._data.values():
            if isinstance(v, Struct):
                if v.embeddings is not None:
                    embeddings.append(v.embeddings)
                    weights.append(1)
                labels.update(v.labels)

        if not embeddings:
            return np.zeros(5), labels

        embeddings = np.array(embeddings)
        weights = np.array(weights)
        weighted_avg = np.average(embeddings, axis=0, weights=weights)
        self.weight = weighted_avg
        self.labels = labels

    def __repr__(self):
        record_values = ", ".join(f"{f}={v!r}" for f, v in self._data.items())
        return f"{self.name}({record_values})"

    def __getnewargs__(self):
        return (self._name, self._data, dict(zip(self._data, self)))

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )

    def __setattr__(self, name, value):
        self._data[name] = value


class Aspect(metaclass=BaseType):
    _context = None
    __slots__ = ()

    def __init__(self, struct: Struct, /, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

        self.peek(struct)

    def walk(self, visited=None) -> Generator[Struct, None, None]:
        if visited is None:
            visited = set()
        if self in visited:
            return

        visited.add(self)
        yield self

        for child in self.children:
            yield from child.walk(visited)
        for sibling in self.siblings:
            if sibling not in visited:
                yield from sibling.walk(visited)
        if self.origin and self.origin not in visited:
            yield from self.origin.walk(visited)

    def peek(self, struct: Struct):
        try:
            struct.share(self)
        except (KeyError, TypeError) as e:
            print(e)

    def visit(self, struct: Struct):
        try:
            struct.accept(self)
        except (KeyError, TypeError) as e:
            print(e)


Action = TypeVar(name="Action")
Result = TypeVar(name="Result")
Parameters = TypeVar(name="Parameters")
Storable = TypeVar(name="Storable", bound=Union[Record, Model])
Actionable = TypeVar(name="Actionable", bound=Union[Aspect, Trait, Tool])
