from __future__ import annotations

from typing import Any, Dict, TypeVar

from scint.api.records import Argument, Arguments
from scint.api.types import Trait

M = TypeVar("M")


class Rules:
    @staticmethod
    def for_component(component_type: str, context: Dict[str, Any] = None):
        rules = {
            "message": message_args,
            "tool": tool_args,
            "agent": agent_args,
        }

        builder = rules.get(component_type, ArgParser)
        if context:
            builder = Rules._apply_context(builder(), context)
        return builder().build()


class ArgParser(Trait):
    def arg(self, name: str, type: str, value: Any = None, req: bool = False):
        self._args.append(Argument(name=name, type=type, value=value, required=req))
        return self

    def kwarg(self, name: str, type_: str, value: Any = None, req: bool = False):
        self._kwargs[name] = Argument(name=name, type=type_, value=value, required=req)
        return self

    def build(self) -> Arguments:
        return Arguments(args=self._args, kwargs=self._kwargs)


def message_args():
    return (
        ArgParser()
        .kwarg("content", "str", required=True)
        .kwarg("role", "str", value="user")
    )


def tool_args():
    return (
        ArgParser()
        .kwarg("name", "str", required=True)
        .kwarg("description", "str", required=True)
        .kwarg("parameters", "dict")
    )


def agent_args():
    return (
        ArgParser()
        .add_kwarg("model", "str", required=True)
        .add_kwarg("temperature", "float", value=0.7)
        .add_kwarg("max_tokens", "int", value=1000)
    )
