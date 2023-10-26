from typing import Any


base_functions: list[dict[str, Any]] = [
    {
        "name": "get_weather",
        "description": "Use this function to get weather data for the specified city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name.",
                },
            },
        },
        "required": ["city"],
    }
]


search: list[dict[str, Any]] = [
    {
        "name": "router",
        "description": ".",
        "parameters": {
            "type": "object",
            "properties": {
                "capability": {
                    "type": "string",
                    "description": "The entity names.",
                    "enum": ["Finder", "Processor", "Generator"],
                },
                "task": {
                    "type": "string",
                    "description": "The task to assign the process. Avoid ambiguity and be as specific as possible, but concise. This also adds a task to your system prompt.",
                },
            },
        },
        "required": ["capability", "task"],
    }
]
