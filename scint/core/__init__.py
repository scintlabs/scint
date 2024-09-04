from functools import wraps
from typing import Type
from uuid import uuid4
from pydantic import Field

from scint.core.utils.logger import logger
from scint.core.utils.helpers import generate_id


__all__ = "context", "App", "Core"


class ContextDict(dict):
    def __init__(self):
        super().__init__()
        self._owner = None
        self._combined = False

    def __getattr__(self, attr):
        if self._combined:
            return (
                getattr(self._owner, attr)
                if hasattr(self._owner, attr)
                else self.get(attr, self)
            )
        return self.get(attr, self)

    def __setattr__(self, name, value):
        if name in ("_owner", "_combined"):
            super().__setattr__(name, value)
        else:
            self[name] = value
            if self._combined and self._owner:
                setattr(self._owner, name, value)

    def __enter__(self):
        self._combined = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._combined = False

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.__exit__(exc_type, exc_val, exc_tb)

    def create(self, name, owner=None):
        new_context = ContextDict()
        new_context._owner = owner
        self[name] = new_context
        return new_context


class ComponentDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return self

    def __setattr__(self, name, value):
        self[name] = value


class ContextType(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return {"compose": ContextDict(), **kwargs}

    def __new__(mcs, name, bases, dct, **kwargs):
        for key, value in dct.items():
            if callable(value):
                dct[key] = mcs.logger(value)

        new_class = super().__new__(mcs, name, bases, dct)
        context = Context()
        new_class._context = context.create_context(new_class)
        return new_class

    @staticmethod
    def logger(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}")
            return func(*args, **kwargs)

        return wrapper


class Context:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.contexts = {}
            cls._instance.classes = {}
        return cls._instance

    def create_context(self, cls: Type) -> ContextDict:
        context = ContextDict()
        context._owner = cls
        self.contexts[cls.__name__] = context
        return context

    def get_context(self, cls: Type) -> ContextDict | None:
        return self.contexts.get(cls.__name__, None)

    def create_class(self, name: str, bases: tuple = (), attrs: dict = None) -> Type:
        attrs = attrs or {}
        attrs["compose"] = lambda self: self._context
        new_class = ContextType(name, bases, attrs)
        self.classes[name] = new_class
        return new_class


def context(cls: Type) -> Type:
    ctx = Context().create_context(cls)
    original_prepare = cls.__prepare__

    @wraps(original_prepare)
    def new_prepare(self, *args, **kwargs):
        dct = original_prepare(self, *args, **kwargs)
        dct["_context"] = ctx
        return dct

    cls.__prepare__ = new_prepare

    def context(self):
        return self._context

    cls.context = context
    return cls


@context
class BaseType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return {"_components": ComponentDict(), **kwds}

    def __new__(cls, name, bases, dct, **kwds):
        for key, value in dct.items():
            if callable(value):
                dct[key] = logger(value)

        def __setattr__(cls, name, value):
            if isinstance(value, BaseType):
                cls._components[name] = value
                value.__set_name__(cls, name)
            super().__setattr__(name, value)

        def _attach(self, name, component):
            if name in self._components:
                self.detach(name)
            setattr(self, name, component)

        def _detach(self, name):
            if name in self._components:
                delattr(self, name)
                del self._components[name]

        def components(self, *args, **kwargs):
            return self._components

        def context(self, *args, **kwargs):
            return self._context

        dct["id"] = generate_id(name)
        dct["context"] = context
        dct["components"] = components
        dct["attach"] = _attach
        dct["detach"] = _detach
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, **kwds):
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Service(metaclass=BaseType):
    def __init__(self, **kwargs):
        self.id: str = Field(default_factory=lambda: str(uuid4()))
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __set_name__(self, owner, name):
        self.name = name


class Core(metaclass=BaseType):
    def __init__(self, **kwargs):
        self.id: str = Field(default_factory=lambda: str(uuid4()))
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
