from enum import Enum
from typing import Any, Dict


from src.core.types import Struct
from src.models.blocks import Block


class Property(Enum):
    string = {"type": "string", "description": ""}
    enum = {"type": "string", "enum": [], "description": ""}
    boolean = {"type": "boolean", "description": ""}
    integer = {"type": "integer", "description": ""}
    array = {"type": "array", "items": [], "description": ""}


class Arguments(Struct):
    properties: Dict[str, Any]


class Result(Struct):
    content: Block


class Function(Struct):
    name: str
    description: str
    parameters: Dict[str, Property]
    code: Block

    @property
    def model(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "parameters": self.parameters,
            },
        }
