compose_structure_output = {
    "name": "composition_schema",
    "schema": {
        "type": "object",
        "properties": {
            "name": {"$ref": "#/$defs/name"},
            "prompt": {
                "type": "string",
                "description": "The high-level instructions for the complete chain of tasks, including the expected final result. This description carries across to every nested task frame.",
            },
            "frames": {
                "type": "array",
                "items": {"$ref": "#/$defs/frame"},
            },
            "interfaces": {"$ref": "#/$defs/interfaces"},
        },
        "required": ["name", "prompt", "frames", "interfaces"],
        "additionalProperties": False,
        "$defs": {
            "name": {
                "type": "string",
                "description": "The name for the given task. It should be relatively short, but memorable and unique as it's used for cross-context communication.",
            },
            "prompt": {
                "type": "string",
                "description": "Task-specific instructions for each frame.",
            },
            "frame": {
                "type": "object",
                "properties": {
                    "name": {"$ref": "#/$defs/name"},
                    "prompt": {"$ref": "#/$defs/prompt"},
                    "frames": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/frame"},
                    },
                    "interfaces": {"$ref": "#/$defs/interfaces"},
                },
                "required": ["name", "prompt", "frames", "interfaces"],
                "additionalProperties": False,
            },
            "interfaces": {
                "type": "array",
                "description": "A selection of tools to use for the task.",
                "items": {"type": "string", "enum": ["Development"]},
            },
        },
    },
    "strict": True,
}

select_agent_output = {
    "name": "composition_schema",
    "schema": {
        "type": "object",
        "properties": {
            "routine": {
                "type": "string",
                "description": "The base routine used to generate intelligent responses.",
                "enum": ["classify", "compose", "parse", "execute", "process"],
            },
            "functions": {
                "type": "array",
                "description": "The functions available to the agent.",
                "items": {
                    "type": "string",
                    "description": "Individual function names.",
                },
            },
            "prompts": {
                "type": "array",
                "description": "The system prompts for this agent.",
                "items": {
                    "type": "string",
                    "description": "Individual prompts.",
                },
            },
            "output": {
                "type": "array",
                "description": "The format of the agent's output messages.",
                "items": {
                    "type": "string",
                    "description": "Individual prompts.",
                },
            },
        },
        "required": ["routine", "functions", "prompts", "output"],
        "additionalProperties": False,
    },
    "strict": True,
}
