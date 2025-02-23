from __future__ import annotations

from uuid import uuid4

from scint.lib.schemas.models import Prompt
from scint.lib.types.tools import Tool
from scint.lib.types.traits import Traits
from scint.lib.types.typing import _finalize_type
from tests.system import Trait


class InterfaceType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        def __init__(self, *args, **kwargs):
            return self.__init_traits__(*args, **kwargs)

        def __init_traits__(self, *args, **kwargs):
            from scint.lib.util.intelligence import Functional

            self._traits = [Functional, *[a for a in args if isinstance(a, Trait)]]
            for t in self._traits:
                other = self
                t.__init_trait__(other)

        def __init_prompts__(self):
            prompts = []
            if dct.get("__doc__"):
                prompts.append(Prompt.from_docstring(dct.get("__doc__")))
            self._prompts = prompts

        def __init_tools__(self):
            tools = {}
            hidden = ("id", "interface", "model", "traits")

            for k, v in dct.items():
                if k in hidden or k.startswith(("_", "__", "__init_")):
                    continue
                if callable(v):
                    tools[k] = Tool(v)
            self._tools = tools

        @property
        def model(self):
            messages = []
            tools = []

            for p in self._prompts:
                messages.append(p.model)
            for t in self._tools.values():
                tools.append(t.model)

            return {
                "messages": messages,
                "tools": tools,
            }

        dct["id"] = str(uuid4())
        dct["type"] = name
        dct["model"] = model
        dct["traits"] = Traits
        dct["__init__"] = __init__
        dct["__init_traits__"] = __init_traits__
        dct["__init_tools__"] = __init_tools__
        dct["__init_prompts__"] = __init_prompts__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Interface(metaclass=InterfaceType): ...
