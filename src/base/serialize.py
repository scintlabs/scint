from __future__ import annotations

import inspect
import textwrap
from enum import Enum
from typing import Any, List, Union, Dict
from typing_extensions import get_args, get_origin

import attrs

_IGNORED = {
    "namespace",
    "base_id",
    "base_ns",
    "kind",
    "created",
    "metadata",
    "_reply_future",
}


def _json_type(tp: Any):
    primitives = {str: "string", int: "integer", float: "number", bool: "boolean"}
    origin, args = get_origin(tp), get_args(tp)

    if origin is Union and type(None) in args:
        return _json_type([a for a in args if a is not type(None)][0])

    if origin in {list, List}:
        return {"type": "array", "items": _json_type(args[0] if args else str)}

    if origin in {dict, Dict}:
        return {"type": "object"}

    if isinstance(tp, type) and issubclass(tp, Enum):
        return {"type": "string", "enum": [e.name for e in tp]}

    return {"type": primitives.get(tp, "string")}


def _param_docs(func):
    doc = textwrap.dedent(inspect.getdoc(func) or "")
    body = next(
        (doc.split(h, 1)[1] for h in ("Args:", "Arguments:", "Parameters") if h in doc),
        "",
    )
    import re

    pat = re.compile(r"^\s*(\w+)\s*:\s*(.+?)(?=\n\s*\w+\s*:|\Z)", re.S | re.M)
    return {n: " ".join(t.split()) for n, t in pat.findall(body)}


def _func_schema(func):
    props, required, docs = {}, [], _param_docs(func)
    for name, p in inspect.signature(func).parameters.items():
        if name in {"self", "cls"}:
            continue

        annot = p.annotation if p.annotation is not inspect._empty else str
        prop = _json_type(annot)

        if docs.get(name):
            prop["description"] = docs[name]
        props[name] = prop

        if p.default is inspect._empty:
            required.append(name)
    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


def _type_schema(cls):
    props, required = {}, []
    for f in attrs.fields(cls):
        if f.name in _IGNORED:
            continue
        props[f.name] = _json_type(f.type) | {
            "description": f.metadata.get("description", f.name)
        }
        required.append(f.name)
    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


def serialize(self, obj: Any):
    if inspect.isfunction(obj):
        return {
            "type": "function",
            "name": obj.__name__,
            "description": (inspect.getdoc(obj) or "").split("\n")[0],
            "parameters": _func_schema(obj),
        }

    if inspect.isclass(obj):
        schema = _type_schema(obj) if attrs.has(obj) else {"type": "object"}
        return {
            "type": "json_schema",
            "name": obj.__name__,
            "schema": schema,
        }

    raise TypeError(f"Unsupported object: {obj!r}")
