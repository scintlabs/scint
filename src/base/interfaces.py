from .models import Memory
from .types import ComposerType


class Composer(metaclass=ComposerType):
    def __init__(self, *args, **kwargs):
        self._context: Memory

    def update(self, context): ...


create_composition = {
    "type": "function",
    "function": {
        "name": "create_composition",
        "description": "Create a composition and pass it to the composer to create a new workflow or process. Use this function when the user requests complex, multi-step tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A short, simple composition name.",
                },
                "description": {
                    "type": "string",
                    "description": "Describe the intent of the composition.",
                },
            },
            "required": ["name", "description"],
            "additionalProperties": False,
        },
    },
}


__all__ = Composer, Memory, create_composition
