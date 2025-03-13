from __future__ import annotations

import inspect
from ast import FunctionType
from enum import Enum, EnumType
from types import MethodType
from typing import Any, Dict
from importlib import import_module

from src.types.models import Model
from src.types.typing import _parse_doc, _parse_params


class FactoryType(EnumType):
    def __call__(cls, *args, **kwargs):
        can_init = len(args) < 3 and isinstance(args[0], str) and callable(args[1])
        if args and not kwargs and can_init:
            return cls._get_init(*args)
        return super().__call__(*args, **kwargs)


class BaseFactory(Enum, metaclass=FactoryType):
    def __init__(self, component_name: str, init_flag=False):
        self.component_name = component_name
        self.init = self._get_init(self.component_name)

    def _get_init(self, component_name: str):
        match component_name:
            case "Agent":
                return BaseFactory.__init_agent__
            case "Routine":
                return BaseFactory.__init_routine__
            case "Function":
                return BaseFactory.__init_function__
            case "Prompt":
                return BaseFactory.__init_prompt__
            case "Output":
                return BaseFactory.__init_output__
            case _:
                raise ValueError(f"Unknown component {component_name}.")

    @staticmethod
    def __init_prompt__(
        other, name: str = None, description: str = None, content: str = None
    ):
        lines = content.strip().split("\n")
        other.name = lines[0].strip()
        other.content = "\n".join(lines[3:]).strip()

    @staticmethod
    def __init_output__(other, format: Dict[str, Any] | Model):
        other.format = format

    @staticmethod
    def __init_function__(other, func: FunctionType):
        desc, _ = _parse_doc(inspect.getdoc(func))
        params = _parse_params(func)
        other.name = func.__name__
        other.description = desc
        other.parameters = params
        other.function = func

    @staticmethod
    def __init_routine__(other, func: FunctionType):
        if callable(func):
            meth = MethodType(func, other)
            other.name = func.__name__
            other.function = meth

    @staticmethod
    def __init_agent__(other, schema: Model):
        module = import_module("src.types.agents")
        routine = getattr(module, "Routine")
        function = getattr(module, "Function")
        prompt = getattr(module, "Prompt")
        output = getattr(module, "Output")
        other.routine = routine(schema.get("routine"))
        other.functions = [function(f) for f in schema.get("functions")]
        other.prompts = [prompt(p) for p in schema.get("prompts")]
        other.output = output(schema.get("output"))
