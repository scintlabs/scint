from __future__ import annotations

from enum import Enum
from functools import wraps
from types import FunctionType
from typing import Any, List, Type, Generic, TypeVar
from attrs import field

from src.runtime.utils import import_object


P = TypeVar("P")
T = TypeVar("T")


class Primitive(Enum):
    Boolean = {"type": "number"}
    Number = {"type": "integer"}
    Float = {"type": "number"}
    String = {"type": "string"}
    List = {"type": "array", "items": {}}
    Dict = {"type": "object", "properties": {}}

    def __init__(self, primitive):
        self.primitive = primitive

    @staticmethod
    def base():
        return {
            "type": "json_schema",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        }

    @staticmethod
    def match(obj: Generic[T]):
        match type(obj):
            case bool():
                return Primitive.Boolean
            case int():
                return Primitive.Number
            case float():
                return Primitive.Float
            case str():
                return Primitive.String
            case list():
                return Primitive.List
            case dict():
                return Primitive.Dict


class Callable(Enum):
    Enum = {"type": "enum", "properties": {}}
    Function = {"type": "function"}
    Interface = {"type": "interface", "properties": {}}

    @staticmethod
    def match(obj: Generic[T]):
        match type(obj):
            case Type():
                return Callable.Class
            case Enum():
                return Callable.Enum
            case FunctionType():
                return Callable.Function


class Format(Enum):
    Message = ("src.model.records", "Message")
    Response = ("src.model.records", "Response")
    Metadata = ("src.model.records", "Metadata")
    Task = ("src.model.outline", "Task")

    def __init__(self, module, obj):
        self.module = module
        self.obj = obj

    def __call__(self):
        return import_object(self.module, self.obj)


class Agent(Enum):
    Composer = ("Execution",)
    Executor = ("Executor",)
    Parser = ("Parser",)
    Observer = ("Observer",)

    def __init__(self, agent_type: str):
        self.agent_type = agent_type

    def __call__(self):
        pass

    async def build(self, message: str, with_context: bool):
        pass


class Parameter(Enum):
    boolean = ("boolean", bool)
    integer = ("integer", int)
    decimal = ("decimal", float)
    string = ("string", str)
    array = ("array", list)
    enum = ("enum", list)
    object = ("object", dict)

    def __init__(self, serialize_name: str, python_type: Type):
        self.serialize_name = serialize_name
        self.python_type = python_type

    def __call__(self, pname: str, desc: str, /, default=None, items: List[Any] = None):
        metadata = {
            "param_type": self,
            "name": pname,
            "description": desc,
            "items": items,
        }

        def validate_type(instance, attribute, value):
            if value is not None and not isinstance(value, self.python_type):
                raise TypeError(
                    f"Expected {self.python_type.__name__} for {attribute.name}, got {type(value).__name__}"
                )

        return field(default=default, metadata=metadata, repr=True)

    def serialize(self, value: Any):
        if value is None:
            return None

        if self == Parameter.array or self == Parameter.enum:
            if not isinstance(value, list):
                raise TypeError(
                    f"Expected list for {self.serialize_name}, got {type(value)}"
                )
            return [self._serialize_item(item) for item in value]

        elif self == Parameter.object:
            if not isinstance(value, dict):
                raise TypeError(
                    f"Expected dict for {self.serialize_name}, got {type(value)}"
                )
            return {k: self._serialize_item(v) for k, v in value.items()}
        return value

    def _serialize_item(self, item: Any):
        if isinstance(item, list):
            return [self._serialize_item(i) for i in item]
        elif isinstance(item, dict):
            return {k: self._serialize_item(v) for k, v in item.items()}
        return item


def _attach_methods(cls, methods: List[Callable]):
    for m in [{m.__name__: m} for m in methods]:
        for k, v in m.items():
            setattr(cls, k, v)
    return cls


def _attach_intercepts(cls, intercepts: List[Callable] = None):
    def decorator(dct, kind, value, callback):
        @wraps
        def wrapped(self, *args, **kwargs):
            for arg in args and kwargs.values():
                if hasattr(arg, kind) and getattr(arg, kind) == value:
                    callback(self, arg)
            return wrapped

        return decorator

    return cls


{
    "type": "function",
    "name": "agent_enum",
    "description": "",
    "parameters": {
        "agent_type": {
            "type": "string",
            "description": "",
            "enum": ["Composer", "Executor", "Parser", "Observer"],
        }
    },
    "required": ["agent_type"],
    "additionalProperties": False,
}
