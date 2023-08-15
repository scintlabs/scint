import json
from typing import NamedTuple, List, Dict, Optional, Any


async def generate_function(cls):
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
