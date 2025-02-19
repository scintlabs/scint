from __future__ import annotations

from ast import FunctionType
from importlib import import_module
from types import MethodType

from scint.lib.types.typing import _build_type


class StructType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        dct = {}
        dct["_fields"] = {}
        dct["_traits"] = {}

        for b in bases:
            if isinstance(b, TraitType):
                dct["_traits"][b.type] = b
            elif isinstance(b, StructType) or issubclass(b, StructType):
                for k, v in b._fields.items():
                    dct["_fields"][k] = v
        return dct

    def __new__(cls, name, bases, dct, **kwds):
        fields = dct.get("_fields")
        traits = dct.get("_traits")

        def __init__(self, *args, **kwargs):
            self._traits = traits
            self.__init_traits__(*args, **kwargs)

        def __init_traits__(self, *args, **kwargs):
            for a in args:
                if a.type == "Trait":
                    other = self
                    a.__init_trait__(other, *args, **kwargs)

        dct["__init__"] = __init__
        dct["__init_traits__"] = __init_traits__
        dct["_fields"] = fields
        dct["traits"] = __init_traits__
        dct = _build_type(name, bases, dct)
        return super().__new__(cls, name, (), dct)


class TraitType(type):
    def __new__(cls, name, bases, dct):
        def __init__(self, other, *args, **kwargs):
            self.__init_trait__(other, *args, **kwargs)

        def __init_trait__(self, other, *args, **kwargs):
            for k, v in dct.items():
                if not k.startswith("_") and isinstance(v, (FunctionType, MethodType)):
                    setattr(other, k, MethodType(v, other))

        dct["__init__"] = __init__
        dct["__init_trait__"] = __init_trait__
        dct = _build_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class ToolsType(StructType):
    def __new__(cls, name, bases, dct):
        tools = {}
        for k, v in dct.items():
            if not k.startswith("_") and callable(v):
                tools[k] = v

        dct["_tools"] = tools
        dct = _build_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class AgentType(StructType):
    def __new__(cls, name, bases, dct, **kwargs):
        def __init__(self, *args, **kwargs):
            self.__init_context__(self, *args, **kwargs)

        def __init_state__(self, *args, **kwargs):
            module = import_module("scint.lib.types.state", "Stateful")
            obj = getattr(module, "Stateful")
            self.state = obj().state

            with self.state.STARTING:
                self.__init_traits__(self, *args, **kwargs)
                self.__init_tools__(self, *args, **kwargs)
                self.__init_context__(self, *args, **kwargs)
            return

        def __init_tools__(self, *args, **kwargs):
            module = import_module("scint.lib.types.tools", "Tools")
            obj = getattr(module, "Tools")
            self.tools = obj(*args, **kwargs)
            return self

        @property
        def model(self):
            return {
                "messages": [m.model for m in self.context.messages],
                "tools": self.tools.model,
            }

        dct["model"] = model
        dct["tools"] = __init_tools__
        dct["__init__"] = __init__
        dct["__init_state__"] = __init_state__
        dct["__init_tools__"] = __init_tools__
        dct = _build_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class ExtensionType(AgentType, StructType): ...
