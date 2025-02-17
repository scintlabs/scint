from __future__ import annotations

import inspect
from ast import FunctionType
from scint.lib.common.typing import List, Optional

from scint.lib.schema import Params
from scint.lib.common.typing import _parse_params, _parse_doc, _finalize_type


class Function:
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
                "parameters": self.parameters.model,
                "strict": True,
            },
        }


class ToolsType(type):
    def __new__(cls, name, bases, dct):
        def model(self):
            return {"tools": [v.model for k, v in self._tools.items()]}

        tools = {}
        for k, v in dct.items():
            if not k.startswith("_") and callable(v):
                tools[k] = Function(v)

        dct["model"] = property(model)
        dct["_tools"] = tools
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Tools(metaclass=ToolsType):
    def __init__(self, *tools):
        self._tools = {}
        self.original_tools = list(tools)
        self.current_tools = []

    def __call__(self, *tools):
        merged_tools = {}
        for tool_class in tools:
            merged_tools.update(tool_class._tools)
        self._tools = merged_tools
        return self


class Task:
    tools = Tools()

    def __init__(self, params: Params = None):
        self.tasks: List[Task] = []
        if params:
            for task in self.params.param:
                self.tasks.append(task)

    async def run(self, context):
        res = await self.process(context)
        context.messages.append(res)
        for task in self.tasks:
            async for res in task.run(context):
                yield res


class Goal: ...
