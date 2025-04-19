from __future__ import annotations

from enum import Enum
from typing import Any, List


class Property(Enum):
    boolean = ("boolean", None)
    integer = ("integer", None)
    decimal = ("decimal", None)
    string = ("string", None)
    array = ("array", None)
    enum = ("enum", None)
    object = ("object", None)

    def __init__(self, *args):
        self.property = args

    def __call__(self, prop_name: str, desc: str, /, items: List[Any] = None):
        ptype, _ = self.property
        return {"type": ptype, "name": prop_name, "description": desc, "items": items}
