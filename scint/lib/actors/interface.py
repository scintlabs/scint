from __future__ import annotations

from uuid import uuid4

from scint.lib.intelligence import Functional
from scint.lib.schema.models import Prompt
from scint.lib.types.tools import Tool
from scint.lib.types.typing import _finalize_type


class InterfaceType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        def __init__(self, *args, **kwargs):
            return self.__init_interface__(*args, **kwargs)

        def __init_interface__(self, *args, **kwargs):
            self.__init_traits__(*args)
            self.__init_prompts__()
            self.__init_tools__()

        def __init_traits__(self, *traits):
            self._traits = [Functional, *[t for t in traits if t.type == "Trait"]]
            for t in self._traits:
                other = self
                t.__init_trait__(other)

        def __init_tools__(self):
            tools = {}
            hidden = ("id", "interface", "model", "traits")

            for k, v in dct.items():
                if k in hidden or k.startswith(("_", "__", "__init_")):
                    continue
                if callable(v):
                    tools[k] = Tool(v)
            self._tools = tools

        def __init_prompts__(self):
            prompts = []
            if dct.get("__doc__"):
                prompts.append(Prompt.from_docstring(dct.get("__doc__")))
            self._prompts = prompts

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
        dct["traits"] = __init_traits__
        dct["interface"] = __init_interface__
        dct["__init__"] = __init__
        dct["__init_traits__"] = __init_traits__
        dct["__init_tools__"] = __init_tools__
        dct["__init_prompts__"] = __init_prompts__
        dct["__init_interface__"] = __init_interface__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Interface(metaclass=InterfaceType): ...
