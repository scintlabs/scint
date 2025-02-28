from __future__ import annotations

from types import MethodType

from src.schemas.state import State
from src.types.signals import SystemMessage
from src.types.traits import Trait
from src.types.typing import _finalize_type


class InterfaceType(type):
    def __new__(cls, name, bases, dct, **kwds):
        def __init__(self, *args, **kwargs):
            self._tools = {}
            self.__init_traits__(*args, **kwargs)

        def __init_traits__(self, *args, **kwargs):
            from src.util.intelligence import Intelligent

            self.traits = [
                Intelligent,
                *[a for a in args if isinstance(a, Trait)],
            ]
            for t in self.traits:
                other = self
                t.__init_trait__(other)

        def __init_tools__(self, *tools):
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
                prompts.append(SystemMessage.from_docstring(dct.get("__doc__")))
            self.prompts = prompts

        dct["type"] = name
        dct["tools"] = __init_tools__
        dct["prompts"] = __init_prompts__
        dct["state"] = State()
        dct["__init__"] = __init__
        dct["__init_traits__"] = __init_traits__
        dct["__init_tools__"] = __init_tools__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Interface(metaclass=InterfaceType):
    def update(self, *args):
        return self.state.update(*args)

    @property
    def model(self):
        return {**self.state.model, "tools": [t.model for t in self._tools.values()]}
