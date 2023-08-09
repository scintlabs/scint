from typing import NamedTuple, List, Dict, Optional
from core.definitions.content import Sentence, Paragraph


def generate_function(cls):
    name = "generate"
    description = f"Use this function to return a {cls} based on the user's input and your functional design."
    parameters = {"type": "object", "properties": cls.properties}
    required = ["content"]

    return [
        {
            "name": name,
            "description": description,
            "parameters": parameters,
            "required": required,
        },
    ]


class Prompt:
    def __init__(
        self,
        identifier: str,
        user_message: bool,
        content: str,
        name: Optional[str] = None,
    ) -> None:
        self.identifier = identifier
        self.content = content
