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


async def eval_function(function: Dict[str, Any]) -> Optional[str]:
    function_name = function["name"]
    function_arguments = function["arguments"]
    data = json.loads(function_arguments)
    content = data.get("content")

    if data.get("function_call"):
        content = await eval_function(data)

    return content
