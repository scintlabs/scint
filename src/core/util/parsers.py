from __future__ import annotations

import ast
import inspect
from typing import Any, Dict, Type
from typing_extensions import get_type_hints


def filter_dunders(attributes: Dict[str, Any]) -> Dict[str, Any]:
    standard_dunders = {
        "__module__",
        "__qualname__",
        "__doc__",
        "__annotations__",
        "__dict__",
        "__weakref__",
        "__classcell__",
    }
    return {
        k: v
        for k, v in attributes.items()
        if not (k in standard_dunders or (k.startswith("__") and k.endswith("__")))
    }


def parse_annotations(cls: Type):
    try:
        type_hints = get_type_hints(cls)
    except (NameError, TypeError):
        type_hints = {}

    raw_annotations = getattr(cls, "__annotations__", {})
    annotations = {}

    for name in set(type_hints.keys()) | set(raw_annotations.keys()):
        if name in type_hints:
            annotations[name] = type_hints[name]
        else:
            annotations[name] = raw_annotations[name]

    return annotations


def parse_attributes(cls: Type, instance=None):
    attributes = {}
    annotations = parse_annotations(cls)

    for k, v in annotations.items():
        if instance and hasattr(instance, k):
            value = getattr(instance, k)
        elif hasattr(cls, k):
            value = getattr(cls, k)
        else:
            value = None
        attributes[k] = (v, value)

    if hasattr(cls, "__dict__"):
        for k, value in cls.__dict__.items():
            if k in attributes or callable(value) or property(value):
                continue
            attributes[k] = (None, value)

    if instance and hasattr(instance, "__dict__"):
        for k, value in instance.__dict__.items():
            if k not in attributes and not callable(value):
                attributes[k] = (None, value)

    return attributes


def parse_callables(cls: Type):
    methods = {}
    try:
        source = inspect.getsource(cls)
        tree = ast.parse(source)
        class_def = None

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == cls.__name__:
                class_def = node
                break

        if class_def:
            for node in class_def.body:
                if isinstance(node, ast.FunctionDef):
                    name = node.name
                    if not (name.startswith("__") and name.endswith("__")):
                        methods.add(name)
    except Exception:
        for k, v in inspect.getmembers(cls):
            if (
                inspect.isfunction(v)
                or inspect.ismethod(v)
                or inspect.ismethodwrapper(v)
                or inspect.ismethoddescriptor(v)
                or inspect.isdatadescriptor(v)
            ) and not (k.startswith("__") and k.endswith("__")):
                methods[k] = v
    return methods


def parse_type(obj: Type, values=False):
    if isinstance(obj, type):
        cls = obj
        instance = None
    else:
        cls = obj.__class__
        instance = obj

    all_attrs = parse_attributes(cls, instance)
    attrs = filter_dunders(all_attrs)
    methods = parse_callables(cls)

    if values:
        vals = {}
        for k, v in attrs.items():
            _, val = v
            vals[k] = val
        return vals, methods
    return attrs, methods
