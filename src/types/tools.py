from __future__ import annotations

import inspect
from ast import FunctionType
import json
from types import MethodType
from typing import Callable

from src.types.signals import ToolCall
from src.types.typing import Optional, Params
from src.types.typing import _parse_params, _parse_doc


class Tool:
    def __init__(self, func: Optional[FunctionType] = None):
        self.name: str = func.__name__
        self.function: Callable = func
        self.description: str
        self.parameters: Params

        if func is not None:
            self.__post_init__(self.function)

    def __post_init__(self, func: FunctionType):
        desc, _ = _parse_doc(inspect.getdoc(func))
        params = _parse_params(func)
        self.name: str = func.__name__
        self.function: Callable = func
        self.description: str = desc
        self.parameters: Params = params
        return self

    def __call__(self, *args, **kwargs):
        if self.function and hasattr(args[0], "function"):
            return self.process(*args)
        if self.function is None and isinstance(args[0], (FunctionType, MethodType)):
            return self.__post_init__(args[0])
        if self.function is None and callable(args[0]) and not kwargs:
            return self

    async def process(self, tool_call: ToolCall):
        call = ToolCall(
            tool_call_id=tool_call.id,
            name=tool_call.function.name,
            arguments=json.loads(tool_call.function.arguments),
        )
        res = self.function(**call.arguments)
        res.tool_call_id = tool_call.id
        return res

    @property
    def model(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {**self.parameters.model},
                "strict": True,
            },
        }


class ToolsType(type):
    def __new__(cls, name, bases, dct):
        def __init_tools__(self, *tools):
            for t in tools:
                for k, v in t._tools.items():
                    self._tools[k] = v

        @property
        def model(self):
            return {"tools": [v.model for k, v in self._tools.items()]}

        tools = {}
        for k, v in dct.items():
            if not k.startswith("_") and callable(v):
                tools[k] = Tool(v)

        dct["model"] = property(model)
        dct["_tools"] = tools
        dct["__init_tools__"] = __init_tools__
        return super().__new__(cls, name, bases, dct)


class Tools(metaclass=ToolsType):
    def __call__(self, *tools):
        return self.__init_tools__(*tools)
