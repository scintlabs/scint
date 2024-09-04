from typing import Any, Callable, Dict

from pydantic import BaseModel


class Function(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]
    arguments: Dict[str, object] = None
    function: Callable = None

    @property
    def index(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
