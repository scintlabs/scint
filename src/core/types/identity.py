from __future__ import annotations
from attrs import define
from uuid import uuid4
from typing import Literal, Callable
from datetime import datetime
from functools import wraps

NamespaceType = Literal["signal", "ensemble", "context", "protocol", "activity"]


def create_identity_decorator(namespace: NamespaceType) -> Callable:
    def decorator(cls):
        prefix = namespace[0].upper()
        name_attr = getattr(cls, "name", "")
        name_suffix = f"_{name_attr}" if name_attr else ""
        cls._id = f"{prefix}{uuid4().hex[:4]}{name_suffix}"
        cls._namespace = namespace
        cls.id = lambda self: self._id
        cls.namespace = lambda self: self._namespace
        cls.__str__ = lambda self: self.id()

        if not hasattr(cls, "__attrs_post_init__"):
            cls.__attrs_post_init__ = lambda self, *args, **kwargs: self
        post_init = cls.__attrs_post_init__

        @wraps(post_init)
        def __attrs_post_init__(self, *args, **kwargs):
            post_init(self, *args, **kwargs)

        cls.__attrs_post_init__ = __attrs_post_init__

        return define(cls)

    return decorator


signal = create_identity_decorator("signal")
ensemble = create_identity_decorator("ensemble")
context = create_identity_decorator("context")
protocol = create_identity_decorator("protocol")
activity = create_identity_decorator("activity")


def tracked_signal(cls):
    cls = define(cls)
    orig_init = cls.__init__

    @wraps(orig_init)
    def __init__(self, *args, **kwargs):
        orig_init(self, *args, **kwargs)

        self.namespace = f"S{uuid4().hex[:4]}"
        self._context = None
        self._protocol = None
        self._activity = None
        self._identity = None
        self._history = {"context": [], "protocol": [], "activity": [], "identity": []}

    cls.__init__ = __init__

    def set_component(self, component_type, obj=None, value=None):
        attr_name = f"_{component_type}"

        if obj is not None:
            component_value = obj.get_id()
        elif value is not None:
            prefix = component_type[0].upper()
            component_value = (
                f"{prefix}{value}" if not value.startswith(prefix) else value
            )
        else:
            raise ValueError("Either obj or value must be provided")

        setattr(self, attr_name, component_value)
        self._history[component_type].append((component_value, datetime.now()))

        return self

    cls.set_component = set_component
    cls.set_context = lambda self, obj: self.set_component("context", obj=obj)
    cls.set_protocol = lambda self, obj: self.set_component("protocol", obj=obj)
    cls.set_activity = lambda self, obj: self.set_component("activity", obj=obj)
    cls.set_identity = lambda self, value: self.set_component("identity", value=value)

    def id(self):
        components = [self.namespace]

        if self._context:
            components.append(self._context)
        if self._protocol:
            components.append(self._protocol)
        if self._activity:
            components.append(self._activity)
        if self._identity:
            components.append(self._identity)

        return "/".join(components)

    def status(self):
        stages = [self._context, self._protocol, self._activity, self._identity]
        return 1 + sum(1 for s in stages if s is not None)

    cls.id = id
    cls.status = status
    cls.__str__ = lambda self: self.get_id()
    return cls
