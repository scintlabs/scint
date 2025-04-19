from __future__ import annotations

import json
import copy
from enum import Enum
from typing import Any, Dict, List, Tuple, Union
from typing_extensions import get_args, get_origin

import attrs

from src.core.util.helpers import timestamp


_BASE = {
    "type": "json_schema",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
}


def _base(name: str) -> Dict[str, Any]:
    schema = copy.deepcopy(_BASE)
    schema["name"] = name.lower()
    return schema


_KIND_DISPATCH = {
    "Tool": lambda o: _base(o.name)
    | {"id": o.id, "description": o.description, "type": "function"},
    "ToolCall": lambda o: {
        "type": "function_call",
        "call_id": o.id,
        "name": o.name,
        "arguments": json.dumps(o.arguments),
    },
    "ToolResult": lambda o: {
        "type": "function_call_output",
        "call_id": o.id,
        "output": f"{timestamp()}\n\n{o.content}",
    },
    "Output": lambda o: _base(o.__name__),
    "Property": lambda o: o,
}


def json_kind(obj: Any) -> Dict[str, Any]:
    tname = type(obj).__name__
    if tname in _KIND_DISPATCH:
        return copy.deepcopy(_KIND_DISPATCH[tname](obj))
    if isinstance(obj, list):
        return json_kind(obj[0])
    return _base(tname)


def json_type(tp: Any) -> Tuple[str, Dict | None]:
    origin = get_origin(tp)
    args = get_args(tp)

    if origin is Union and type(None) in args:
        non_null = [a for a in args if a is not type(None)][0]
        return json_type(non_null)

    if origin in (list, List):
        item_type = args[0] if args else str
        item_jtype, item_extra = json_type(item_type)
        items_schema = {"type": item_jtype}
        if item_extra:
            items_schema |= item_extra
        return "array", {"items": items_schema}

    if origin in (dict, Dict):
        return "object", {}

    if tp in (str, int, float, bool):
        return {str: "string", int: "integer", float: "number", bool: "boolean"}[
            tp
        ], None

    if isinstance(tp, type) and issubclass(tp, Enum):
        return "string", {"enum": [e.name for e in tp]}

    if attrs.has(tp):
        return "object", build_object(tp)["schema"]

    return "string", None


def _is_optional(tp: Any) -> bool:
    origin = get_origin(tp)
    return origin is Union and type(None) in get_args(tp)


def build_object(cls: type) -> Dict[str, Any]:
    schema = _base(cls.__name__)

    for fld in attrs.fields(cls):
        j_type, extra = json_type(fld.type)
        prop = {
            "type": j_type,
            "description": fld.metadata.get("description", fld.name),
        }
        if extra:
            prop |= extra
        schema["schema"]["properties"][fld.name] = prop

        if not _is_optional(fld.type) and fld.default is attrs.NOTHING:
            schema["schema"]["required"].append(fld.name)

    return schema


def transform(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict) and obj.get("type") in {
        "boolean",
        "integer",
        "decimal",
        "string",
        "array",
        "enum",
        "object",
    }:
        return obj

    base = json_kind(obj)

    if "schema" in base and base["schema"]["properties"]:
        return base

    target_cls = obj if isinstance(obj, type) else type(obj)
    if attrs.has(target_cls):
        populated = build_object(target_cls)
        base["schema"] = populated["schema"]

    return base
