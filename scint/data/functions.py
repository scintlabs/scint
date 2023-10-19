from typing import Any

router: list[dict[str, Any]] = [
    {
        "name": "capabilities",
        "description": "Activate Scint's enhanced capabilities to plan, create, work, research, and learn—and to help users do the same.",
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


capabilities: list[dict[str, Any]] = [
    {
        "name": "init_capabilities",
        "description": "When a user asks for advanced capabilities, such as file access or information search, call this function.",
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
