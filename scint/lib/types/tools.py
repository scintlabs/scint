from __future__ import annotations

import inspect
from ast import FunctionType

from scint.lib.types.typing import Optional
from scint.lib.types.typing import _parse_params, _parse_doc


class Tool:
    def __init__(self, func: Optional[FunctionType] = None):
        self.name = func.__name__
        self.function = func
        self.description = None
        self.parameters = None
        if func is not None:
            self.__post_init__(self.function)

    def __call__(self, *args, **kwargs):
        if self.function is None and callable(args[0]) and not kwargs:
            return self.__post_init__(args[0])
        return self.function(*args, **kwargs)

    def __post_init__(self, func: FunctionType):
        desc, _ = _parse_doc(inspect.getdoc(func))
        params = _parse_params(func)
        self.name = func.__name__
        self.function = func
        self.description = desc
        self.parameters = params
        return self

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
        def model(self):
            return {"tools": [v.model for k, v in self._tools.items()]}

        def __init_tools__(self, *tools):
            for t in tools:
                for k, v in t._tools.items():
                    self._tools[k] = v

        def __init_toolkit__(self, *tools):
            for t in tools:
                for k, v in t._tools.items():
                    self._tools[k] = v

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


class ToolKit(metaclass=ToolsType):
    def __call__(self, *tools):
        return self.__init_toolkit__(*tools)
