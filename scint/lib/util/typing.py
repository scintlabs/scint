from __future__ import annotations

import inspect
from enum import Enum, EnumType
from types import FunctionType, new_class, prepare_class
from uuid import uuid4
from typing import Any, Dict, List, Literal, Optional, Type, Union, Tuple
from typing_extensions import TypeVar, get_args, get_origin

from scint.lib.schema.models import Model, Param, Params

_I = TypeVar("_I")
_Tr = TypeVar("_Tr")
_Tl = TypeVar("_Tl")
_S = TypeVar("_S")
_M = TypeVar("_M")


def _parse_doc(doc: Optional[str]) -> Tuple[str, Dict[str, str]]:
    if not doc:
        return "", {}

    lines = [line.strip() for line in doc.splitlines() if line.strip()]
    if not lines:
        return "", {}

    description = lines[0]
    param_descs = {}

    for line in lines[1:]:
        if ":" in line:
            param, desc = line.split(":", 1)
            param_descs[param.strip()] = desc.strip()
    return description, param_descs


def _parse_annotation(annotation: Any) -> Optional[Dict[str, Any]]:
    if annotation == inspect.Parameter.empty:
        return None

    origin = get_origin(annotation)
    args = get_args(annotation)

    if annotation in (str, int, bool, float):
        return {"type": annotation.__name__}

    if origin is Literal:
        return {"enum": list(args)}

    if origin in (list, List):
        item_schema = _parse_annotation(args[0]) if args else {}
        return {"type": "array", "items": item_schema}

    if origin in (dict, Dict):
        if len(args) == 2:
            _, value_type = args
            value_schema = _parse_annotation(value_type)
        else:
            value_schema = {}
        return {"type": "object", "additionalProperties": value_schema}

    if inspect.isclass(annotation) and issubclass(annotation, Model):
        return {"type": "object", "properties": annotation().model}

    if origin is Union:
        models = []
        for arg in args:
            if arg is type(None):
                models.append({"type": "null"})
            else:
                arg_schema = _parse_annotation(arg)
                if arg_schema:
                    models.append(arg_schema)
        return {"oneOf": models}

    if inspect.isclass(annotation) and issubclass(annotation, Enum):
        enum_values = [item.value for item in annotation]
        return {"type": "string", "enum": enum_values}

    return None


def _parse_params(func: FunctionType) -> "Params":
    if func is None:
        return None
    sig = inspect.signature(func)
    doc = inspect.getdoc(func)
    _, param_descs = _parse_doc(doc)
    parameters_list: List[Param] = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        schema = _parse_annotation(param.annotation)
        if not schema:
            continue

        ptype = schema.get("type", "")
        if "enum" in schema:
            ptype = "enum"
            items = schema["enum"]
        elif ptype == "array":
            items = schema.get("items", None)
        else:
            items = None

        prop_desc = param_descs.get(name, "")
        if not prop_desc and schema.get("enum"):
            prop_desc = f"Possible values: {schema['enum']}"

        parameters_list.append(
            Param(
                name=name,
                type=ptype,
                description=prop_desc,
                items=items,
            )
        )

    return Params(parameters=parameters_list)


def _create_service(name, bases, dct):
    service = dct.get("type")
    interface = dct.get("interface")
    manager = dct.get("manager", None)

    if service and interface:
        interface_name = f"{service.lower()}"

        def __init__(self, *args, **kwargs):
            original_init = dct.get("__init__")
            if original_init:
                original_init(self, *args, **kwargs)

            interface_instance = interface.new()
            setattr(self, f"_{interface_name}", interface_instance)

            if manager:
                manager_instance = manager()
                setattr(self, f"_{interface_name}_manager", manager_instance)

            def get_interface(self):
                return getattr(self, f"_{interface_name}")

            setattr(self.__class__, interface_name, property(get_interface))

        dct["__init__"] = __init__
    return _finalize_type(name, bases, dct)


def _create_interface(name: str, bases, dct: Dict[str, Any]):
    dct["id"] = str(uuid4())
    dct["name"] = name
    return _finalize_type(name, bases, dct)


def _create_struct(name: str, bases, dct: Dict[str, Any]):
    def __init__(self, *args, **kwargs):
        self._data = self.__dict__

    def __post_init__(self, **kwargs):
        for f, t in annotations.items():
            if f not in kwargs:
                raise TypeError(f"Missing required argument: {f}")
            value = kwargs[f]
            if not _validate_type(value, t):
                raise TypeError(f"Expected {t} for {f}, got {type(value)}")
            self._data[f] = value

    def __repr__(self):
        fields = [f"{k}={self._data[k]!r}" for k in self._data]
        return f"{self.__class__.__name__}({', '.join(fields)})"

    dct["__init__"] = __init__
    dct["__post_init__"] = __post_init__
    dct["__repr__"] = __repr__
    return _finalize_type(name, bases, dct)


def _create_tool(name: str, bases, dct: Dict[str, Any]):
    return _finalize_type(name, bases, dct)


def _define_type(name, type, **kwds):
    return prepare_class(name + "Type", (type,), kwds)


def _with_context(dct: Dict[str, Any]):
    # def __getattr__(self, key):
    #     try:
    #         if key in self._context:
    #             return key
    #     except KeyError:
    #         raise KeyError(f"No '{key}' attribute found in '{self}'.")

    # def __setattr__(self, key, val):
    #     try:
    #         if key in self._context:
    #             self._context[key] = val
    #     except KeyError:
    #         raise KeyError(f"No '{key}' attribute found in '{self}'.")

    # dct["_context"] = {}
    # dct["__getattr__"] = __getattr__
    # dct["__setattr__"] = __setattr__
    return dct


def _with_traits(dct):
    pass


def _with_constructor(dct):
    pass


def _build_type(name, bases, kwds, namespace):
    return new_class("Base" + name, bases, kwds, lambda ns: ns.update(namespace))


def _validate_type(value, expected_type):
    origin = get_origin(expected_type)
    if origin is not None:
        args = get_args(expected_type)
        if origin in (list, List):
            if not isinstance(value, list):
                return False
            return all(isinstance(item, args[0]) for item in value)
        return True
    return isinstance(value, expected_type)


def _finalize_type(name: str, bases: Tuple[Type], dct: Dict[str, Any]):
    if any(hasattr(b, "id") for b in bases):
        dct["__init_subclass__"] = lambda self, **kwargs: None
        dct["__subclasscheck__"] = lambda *args: False
    return dct


class ConstructorType(EnumType):
    def __call__(cls, *args, **kwargs):
        if (
            args
            and len(args) >= 3
            and isinstance(args[0], str)
            and isinstance(args[1], tuple)
            and isinstance(args[2], dict)
        ):
            return cls._make(*args, **kwargs)
        else:
            return super().__call__(*args, **kwargs)


class Constructor(Enum, metaclass=ConstructorType):
    def __init__(self, name=False, bases=False, dct=False, new=False):
        self.type_name = name
        self.base = bases
        self.dct = dct
        self.new = self.__call__(name, bases, dct)

    def __call__(self, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        dct = self._get_type(name, bases, dct)
        return new_class(name, bases, {}, lambda ns: dct)

    def _get_type(self, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        from importlib import import_module

        try:
            match name:
                case "Entity":
                    module = import_module("scint.lib.entities", "Handler")
                    return getattr(module, name)
                case "Thread":
                    module = import_module("scint.lib.context", "Thread")
                    return getattr(module, name)
                case _:
                    return _create_tool(name, bases, dct)
        except Exception as e:
            raise Exception(f"Couldn't create type '{name}': {e}.")

    @classmethod
    def _make(cls, name: str, bases: Tuple[Type], dct: Dict[str, Any]):
        member = next(iter(cls))
        return member.__call__(name, bases, dct)


# class ServiceTypes(Constructor):
# Caching = ("Caching", (), {})
# Composer = ("Composer", (), {})
# Exchange = ("Exchange", (), {})
# Indexing = ("Indexing", (), {})
# Intelligence = ("Intelligence", (), {})
# Observability = ("Observability", (), {})
# Storage = ("Storage", (), {})


# class Providers(Constructor):
# LocalStorage = ("LocalStorage", (), {})
# OpenAI = ("OpenAI", (), {})
# Anthropic = ("Anthropic", (), {})
# Redis = ("Redis", (), {})
