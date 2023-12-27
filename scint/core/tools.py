import json
from typing import Any, Dict, List

from scint.services.logger import log


class ToolMeta(type):
    def __new__(cls, name, bases, dct):
        if "metadata" not in dct:
            dct["metadata"] = cls.data_dump(name, dct)

        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def data_dump(name, dct):
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": dct.get("description", "No description provided"),
                "properties": dct.get("props", {}),
                "required": dct.get("required", []),
            },
        }


class Tool(metaclass=ToolMeta):
    pass


class Tools:
    def __init__(self, tools: List[Tool] = None):
        if tools is None:
            tools = []
        self._tools = tools

    def add(self, tool: Tool):
        self._tools.append(tool)

    def remove(self, tool):
        self._tools = [t for t in self._tools if t != tool]

    def data_dump(self) -> List[Dict[str, Any]]:
        return [
            tool.__class__.data_dump(tool.__class__.__name__, tool.__class__.__dict__)
            for tool in self._tools
        ]

    def __iter__(self):
        return iter(self._tools)
