import json
from typing import Any, Dict, List, Optional

from scint.services.logger import log


class ToolMeta(type):
    def __new__(cls, name, bases, dct):
        if "metadata" not in dct:
            dct["metadata"] = cls.data_dump(name, dct)

        return super().__new__(cls, name, bases, dct)

    @classmethod
    def data_dump(cls, name, dct):
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": dct.get("description", ""),
                "parameters": {
                    "type": "object",
                    "properties": dct.get("props", {}),
                    "required": dct.get("required", []),
                },
            },
        }

    @classmethod
    async def validate_tool_call(cls, tool_call):
        try:
            func = tool_call.get("function")
            func_args = json.loads(func.get("arguments"))

            async for response in cls.execute_action(**func_args):
                yield response

        except Exception as e:
            log.error(f"{cls.__name__}: {e}")


class Tool(metaclass=ToolMeta):
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = None
        self.props = None
        self.required = None

    async def execute_action(self, **kwargs):
        raise NotImplementedError("This method should be overridden in the subclass.")


class Tools:
    def __init__(self, tools: List[Tool] = []):
        self._tools = tools

    def __iter__(self):
        return iter(self._tools)

    def add(self, tool: Tool):
        self._tools.append(tool)

    def remove(self, tool):
        self._tools = [t for t in self._tools if t != tool]

    def get(self, tool_name: str) -> Optional[Tool]:
        for tool in self._tools:
            if tool.name == tool_name:
                return tool
        return None

    def data_dump(self) -> List[Dict[str, Any]]:
        return [
            tool.__class__.data_dump(tool.__class__.__name__, tool.__class__.__dict__)
            for tool in self._tools
        ]
