from __future__ import annotations

from types import MethodType, new_class
from typing import List

from scint.lib.schemas.context import ContextConnector
from scint.lib.schemas.signals import Prompt
from scint.lib.types.traits import Trait
from scint.lib.types.enum import Factory
from scint.lib.types.typing import _finalize_type


# class Parameters(Model):
#     interface: Any
#     traits: Any
#     prompts: Any
#     tools: Any
#     interface: Any


class PrototypeMeta(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        bases = tuple(b for b in bases if not isinstance(b, Trait))
        traits = (b for b in bases if isinstance(b, Trait))
        return super().__prepare__(name, bases, {"traits": traits})

    def __new__(cls, name, bases, dct, **kwds):
        def __init__(self, *args, **kwargs):
            traits = kwds.get("traits", [])

            for a in args:
                if isinstance(a, Trait):
                    traits.append(a)
            self.__init_traits__(traits)

        def __init_traits__(self, traits: List[Trait] = None):
            from scint.lib.util.intelligence import Intelligent

            self._traits = [Intelligent, *traits]
            for t in self._traits:
                other = self
                t.__init_trait__(other)

        def __init_tools__(self, *tools):
            if not hasattr(self, "_tools"):
                self._tools = {}

            for k, v in self._tools.items():
                if hasattr(self, k):
                    if getattr(self, k) == v:
                        delattr(self, k)

            for t in tools:
                self._tools.update(t._tools)
                for k, v in self._tools.items():
                    func = v
                    setattr(self, k, MethodType(func, self))

        def __init_prompts__(self):
            prompts = []
            if dct.get("__doc__"):
                prompts.append(Prompt.from_docstring(dct.get("__doc__")))
            self._prompts = prompts

        dct["type"] = name
        dct["context"] = ContextConnector()
        dct["traits"] = __init_traits__
        dct["tools"] = __init_tools__
        dct["prompts"] = __init_prompts__
        dct["__init_traits__"] = __init_traits__
        dct["__init__"] = __init__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Prototype(metaclass=PrototypeMeta):
    def update(self, *args):
        return self.context.update(self.type, *args)

    @property
    def model(self):
        return {
            **self.context.model,
            "tools": [t.model for t in self._tools.values()],
        }


def prototype(name, *args, **kwargs):
    def _set_traits(dct):
        def __init_traits__(self, traits: List[Trait] = None):
            from importlib import import_module

            module = import_module("scint.lib.util.intelligence")
            intelligence = getattr(module, "Intelligent")

            self._traits = [intelligence, *traits]
            for t in self._traits:
                other = self
                t.__init_trait__(other)

        dct["traits"] = __init_traits__
        dct["__init_traits__"] = __init_traits__
        return dct

    def _set_tools(dct):
        def __init_tools__(self, *tools):
            self._tools = {}

            for k, v in self._tools.items():
                if hasattr(self, k):
                    if getattr(self, k) == v:
                        delattr(self, k)

            for t in tools:
                self._tools.update(t._tools)
                for k, v in self._tools.items():
                    func = v
                    setattr(self, k, MethodType(func, self))

        dct["tools"] = __init_tools__
        return dct

    def _set_prompts(dct):
        def __init_prompts__(self):
            prompts = []
            if dct.get("__doc__") is not None:
                prompts.append(Prompt.from_docstring(dct.get("__doc__")))
                self._prompts = prompts

        dct["prompts"] = __init_prompts__
        return dct

    def update(self, *args):
        return self.context.update(self, *args)

    @property
    def model(self):
        return {
            **self.context.model,
            "tools": [t.model for t in self._tools.values()],
        }

    name = name
    bases = ()
    dct = {
        "context": ContextConnector(),
        "update": update,
        "model": model,
    }
    dct = _set_traits(dct)
    dct = _set_tools(dct)
    dct = _set_prompts(dct)
    dct = _finalize_type(name, bases, dct)
    cls = new_class(name, (), {"metaclass": PrototypeMeta}, lambda ns: ns.update(dct))
    return cls()


class PrototypeFactory(Factory):
    Parser = ("Parser", (Prototype,), {})
    Handler = ("Handler", (Prototype,), {})
    Interpreter = ("Interpreter", (Prototype,), {})
