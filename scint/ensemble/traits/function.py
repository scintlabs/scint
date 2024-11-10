from ast import FunctionType
from types import MethodType
from typing import Any, Dict

from scint.ensemble.traits.base import Trait


class Function(Trait):
    name: str
    description: str
    parameters: Dict[str, Any]
    function: FunctionType

    async def invoke(self, function, *args, **kwargs):
        return await function(*args, **kwargs)


class Method(Trait):
    name: str
    description: str
    parameters: Dict[str, Any]
    function: MethodType

    async def invoke(self, function, *args, **kwargs):
        return await function(*args, **kwargs)


class Callback(Trait):
    name: str
    description: str
    parameters: Dict[str, Any]
    function: FunctionType

    async def invoke(self, function, *args, **kwargs):
        return await function(*args, **kwargs)
