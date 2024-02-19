import inspect
import uuid
from ctypes import Union
from typing import List, Optional, get_args, get_origin

import injector
from pydantic import BaseModel

from scint.components.config import Preset
from scint.utils.logger import log


def is_optional_annotation(annotation):
    return get_origin(annotation) is Union and type(None) in get_args(annotation)


class ToolMeta(type):
    @classmethod
    def __prepare__(mcls, __name, __bases, **kwargs):
        return super().__prepare__(__name, __bases, **kwargs)

    def __new__(cls, name, bases, dct, **kwargs):
        dct["name"] = name
        dct["id"] = uuid.uuid4()
        dct["preset"] = Preset.tool
        original_function = dct["function"]
        func_signature = inspect.signature(original_function)
        required_params = [
            name
            for name, param in func_signature.parameters.items()
            if param.default == inspect.Parameter.empty
            and name != "self"
            and param != None
        ]

        dct["dictionary"] = cls.model_dump(name, dct, required_params)
        return super().__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance

    @classmethod
    def model_dump(cls, name, dct, required_params):
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": dct.get("description"),
                "parameters": {
                    "type": "object",
                    "properties": dct.get("props", {}),
                    "required": required_params,
                },
            },
        }


class Tool(metaclass=ToolMeta):
    description = None
    props = None

    async def function(self):
        yield NotImplementedError("This method should be overridden in the subclass.")


class Tools(BaseModel):
    name: str
    tools: List[Tool] = []

    class Config:
        arbitrary_types_allowed = True

    def get_tool(self, name: str) -> Tool:
        for tool_instance in self.tools:
            if getattr(tool_instance, "name", None) == name:
                return tool_instance
        return None

    def model_dump(self):
        return [tool.dictionary for tool in self.tools]


class IToolsProvider:
    def register(self, name, tooling):
        pass


class ToolsProvider(IToolsProvider):
    @injector.inject
    def __init__(self):
        self.id = uuid.uuid4()
        self.tools_directory: List[Tools] = []
        self.tools_instances: List[Tools] = []

    def register(self, name: str, tooling: str):
        tools_instance = Tools(name=name)
        for tool in tooling:
            tools_instance.tools.append(tool)

        self.tools_instances.append(tools_instance)
        return self.get_tools_instance(name)

    def get_tools_instance(self, name: str) -> List[Tool]:
        for tools_instance in self.tools_instances:
            if tools_instance.name == name:
                return tools_instance

    def model_dump(self):
        return [tool.dictionary for tool in self._tools]


class ToolsModule(injector.Module):
    @injector.provider
    def context_provider(self) -> IToolsProvider:
        return ToolsProvider()

    def configure(self, binder: injector.Binder) -> None:
        binder.bind(IToolsProvider, to=ToolsProvider)
