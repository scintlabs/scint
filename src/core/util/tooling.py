from __future__ import annotations

import ast
import hashlib
import inspect
import json
import functools
import pathlib
import textwrap
from enum import Enum
import re
from typing import Any, Dict, List, Union, get_args, get_origin

import attrs

from src.core.util.llms import generate_desc

COMP_PATH = pathlib.Path("config/components.json")
COMP_PATH.parent.mkdir(parents=True, exist_ok=True)

if not COMP_PATH.exists():
    COMP_PATH.write_text('{"tools": {}}', encoding="utf‑8")

_JS_PRIMS = {str: "string", int: "integer", float: "number", bool: "boolean"}


_PARAM_PATTERNS = [
    re.compile(r"^\s*(\w+)\s*:\s*[^\n]+\n\s*(.+?)(?=\n\s*\w+\s*:|\Z)", re.S | re.M),
    re.compile(r"^\s*:param\s+(\w+)\s*:\s*(.+?)(?=\n\s*:param|\Z)", re.S | re.M),
]


def _extract_param_docs(func) -> dict[str, str]:
    doc = inspect.getdoc(func) or ""
    if not doc:
        return {}

    doc = textwrap.dedent(doc)
    for header in ("Args:", "Arguments:", "Parameters"):
        if header in doc:
            doc = doc.split(header, 1)[1]

    descs = {}
    for pat in _PARAM_PATTERNS:
        for name, text in pat.findall(doc):
            descs[name] = " ".join(text.strip().split())
    return descs


def _func_fingerprint(fn: callable) -> str:
    node = ast.parse(inspect.getsource(fn)).body[0]
    node.body = []
    digest = hashlib.sha1(ast.unparse(node).encode()).hexdigest()
    return digest


def _json_type(tp: Any) -> Dict[str, Any]:
    origin, args = get_origin(tp), get_args(tp)

    if origin is Union and type(None) in args:
        return _json_type([a for a in args if a is not type(None)][0])

    if origin in (list, List):
        item_schema = _json_type(args[0] if args else str)
        return {"type": "array", "items": item_schema}

    if origin in (dict, Dict):
        return {"type": "object"}

    if tp in _JS_PRIMS:
        return {"type": _JS_PRIMS[tp]}

    if isinstance(tp, type) and issubclass(tp, Enum):
        return {"type": "string", "enum": [e.name for e in tp]}

    if attrs.has(tp):
        return _attrs_to_schema(tp)["schema"]

    return {"type": "string"}


def _attrs_to_schema(cls) -> Dict[str, Any]:
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }
    for fld in attrs.fields(cls):
        schema["properties"][fld.name] = _json_type(fld.type) | {
            "description": fld.metadata.get("description", fld.name)
        }
        if getattr(fld, "default", attrs.NOTHING) is attrs.NOTHING and not (
            get_origin(fld.type) is Union and type(None) in get_args(fld.type)
        ):
            schema["required"].append(fld.name)
    return {"schema": schema}


def _parse_signature(func) -> Dict[str, Any]:
    sig = inspect.signature(func)
    param_docs = _extract_param_docs(func)

    props, required = {}, []
    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue

        annot = param.annotation if param.annotation is not inspect._empty else str
        schema_frag = _json_type(annot)
        desc = param_docs.get(name)

        if not desc:
            desc = generate_desc(name, kind="parameter")

        schema_frag["description"] = desc
        props[name] = schema_frag

        if param.default is inspect._empty:
            required.append(name)

    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


def _load_components() -> Dict[str, Any]:
    return json.loads(COMP_PATH.read_text(encoding="utf‑8"))


def _store_components(data: Dict[str, Any]):
    COMP_PATH.write_text(json.dumps(data, indent=2), encoding="utf‑8")


def build_tool_schema(func) -> Dict[str, Any]:
    comps = _load_components()

    cache = next(
        (t for t in comps["tools"] if t["schema"]["name"] == func.__name__), None
    )

    sig_fingerprint = _func_fingerprint(func)

    if cache and cache.get("_sig") == sig_fingerprint:
        return cache["schema"]

    desc = inspect.getdoc(func) or generate_desc(inspect.getsource(func), "function")

    schema = {
        "type": "function",
        "name": func.__name__,
        "description": desc,
        "parameters": _parse_signature(func),
    }

    if cache:
        cache.update({"_sig": sig_fingerprint, "schema": schema})
    else:
        comps["tools"].append({"_sig": sig_fingerprint, "schema": schema})

    _store_components(comps)
    return schema


def tool(func):
    schema = build_tool_schema(func)

    async def _exec(agent, tool_call):
        if tool_call.name != func.__name__:
            return
        args = json.loads(tool_call.arguments)
        res = await func(**args) if inspect.iscoroutinefunction(func) else func(**args)
        res.id = tool_call.id
        agent.input.extend([tool_call, res])
        async for resp in agent.evaluate():
            yield resp

    @functools.wraps(func)
    def dispatcher(*args, **kwargs):
        if not args and not kwargs:
            return schema
        if len(args) == 2 and hasattr(args[1], "arguments"):
            return _exec(*args)
        return func(*args, **kwargs)

    dispatcher.schema = schema
    dispatcher.exec = _exec
    return dispatcher
