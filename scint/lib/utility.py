from __future__ import annotations

from types import MethodType
from scint.lib.util.typing import Any, List


from scint.lib.tools import Tool


class Requires:
    def __init__(self, *requirements: List[Any]):
        self.name = "_requires"
        self.requirements = list(requirements)

    def __set_name__(self, instance, owner):
        self.owner = owner

    def __get__(self, instance, owner):
        if instance is None:
            return self

        for obj in self.requirements:
            for tool in getattr(obj, "_tools"):
                if isinstance(tool, Tool) and tool.description is not None:
                    instance.tools.append(tool)

            for k, v in getattr(obj, "_functions").items():
                meth = MethodType(v, instance)
                setattr(instance, k, meth)
        return self
