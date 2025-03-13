from __future__ import annotations

import inspect
from enum import Enum
from types import FunctionType
from typing import Any, Dict, List, Literal, Optional, Type, Union, Tuple
from typing_extensions import get_args, get_origin

from pydantic import BaseModel


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

    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
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


def _parse_params(func: FunctionType):
    from src.types.agents import Param, Params

    if func is None:
        return None
    sig = inspect.signature(func)
    doc = inspect.getdoc(func)
    _, param_descs = _parse_doc(doc)
    params: List[Param] = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue
        schema = _parse_annotation(param.annotation)
        if not schema:
            continue
        if not schema.get("type"):
            return

        match schema.get("type", ""):
            case "str":
                ptype = "string"
            case "int":
                ptype = "integer"
            case "float":
                ptype = "number"
            case "bool":
                ptype = "boolean"
            case "list":
                ptype = "array"
            case "dict":
                ptype = "object"
            case "None":
                ptype = "null"
            case _:
                ptype = "string"

        if "enum" in schema:
            ptype = "enum"
            items = schema["enum"]
        elif ptype == "array":
            items = schema.get("items", None)
        else:
            items = None

        prop_desc = param_descs.get(name, "")
        params.append(Param(name=name, type=ptype, description=prop_desc, items=items))

    return Params(parameters=params)


def _finalize_type(name: str, bases: Tuple[Type], dct: Dict[str, Any]):
    if any(b for b in bases):
        dct["__init_subclass__"] = lambda self, **kwargs: None
        dct["__subclasscheck__"] = lambda *args: False
    return dct
