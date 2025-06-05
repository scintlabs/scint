from __future__ import annotations

import copy
from enum import Enum
from types import FunctionType
from typing import Any, List, Type, Generic, TypeVar

from attrs import field, validators


T = TypeVar("T")


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

        return field(
            default=default,
            metadata=metadata,
            validator=validators.optional(validate_type),
            repr=True,
        )

    def serialize(self, value: Any) -> Any:
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


class Serializer(Enum):
    Message = (lambda o: Serializer.get_schema(type(o).__name__),)
    Function = (lambda o: Serializer.get_schema(o.name),)
    Property = (lambda o: o,)

    def __init__(self, build):
        self.build = build

    def get_schema(self, name: str):
        schema = copy.deepcopy(Primitive.base())
        schema["name"] = name.lower()
        return schema
