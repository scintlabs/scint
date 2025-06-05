from __future__ import annotations

import inspect
from uuid import uuid4
from functools import wraps
from typing import Callable, Any, Dict, List, Type

from attrs import define, field

from .serialize import serialize
from .utils import import_object, timestamp
from .records import Instructions


def _generate_id(name: str) -> str:
    return f"{name[:2].upper()}-{uuid4().hex[:4]}"


def _attach(cls: Type, attrs_: Dict[str, Any]) -> Type:
    for k, v in attrs_.items():
        setattr(cls, k, v)
    return cls


def _maybe_copy_proto(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {k: (v[:] if isinstance(v, list) else v) for k, v in meta.items()}


async def _maybe_await(x):
    if inspect.isawaitable(x):
        await x


def resolve_location(self, other):
    if hasattr(other, "_protocol"):
        other_base = getattr(other, "_protocol")["id"][0]
        (self._protocol["id"].append(other_base) if other_base is not None else None)
        self._protocol["history"].append(
            {other._protocol["name"]: other_base, "added": timestamp()}
        )


def _metaprotocol(cls, name: str):
    dct = {}
    dct["id"] = [f"{name[:2].upper()}-{uuid4().hex[:4]}"]
    dct["protocols"] = [name]
    dct["history"] = []

    config = import_object("src.runtime.intelligence", "ModelConfig")
    generate = import_object("src.runtime.intelligence", "generate")
    methods = [id, generate, serialize]

    attributes = {
        "_protocol": field(type=Dict[str, Any], default=dct),
        "config": config(),
    }

    cls = _set_attributes(cls, attributes)
    return _attach_methods(cls, methods)


def _set_attributes(cls, attrs: Dict[str, Any]):
    for k, v in attrs.items():
        setattr(cls, k, v)
    return cls


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


def protocol(key: str, attrs: Dict[str, Any], methods: List[Callable]):
    def decorator(cls):
        cls = _metaprotocol(cls, key)
        cls = _set_attributes(cls, attrs)
        cls = _attach_methods(cls, methods)
        return define(cls)

    return decorator


@define
class Intercept:
    def before_call(self, obj: Callable = None): ...
    def after_call(self, obj: Callable = None): ...
    def on_exception(self, obj: Callable = None): ...
    def on_event(self, obj: Callable = None): ...


agentic = protocol("agentic", {"instructions": Instructions}, [])
