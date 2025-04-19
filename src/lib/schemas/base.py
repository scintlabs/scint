from __future__ import annotations


input_message = {
    "type": "json_schema",
    "name": "input_message",
    "schema": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The sender of the message",
            },
            "sender": {
                "type": "string",
                "description": "The sender of the message",
            },
            "content": {
                "type": "string",
                "description": "Message content.",
                "items": {"type": "string"},
            },
            "embedding": {
                "type": "array",
                "description": "A semantic embedding of the message's content.",
                "items": {"type": "integer"},
            },
        },
        "required": ["id", "sender", "content"],
        "additionalProperties": False,
    },
    "strict": True,
}

output_message = {
    "type": "json_schema",
    "name": "output_message",
    "schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "array",
                "description": "A list of messages, where each message represents a lexical, markdown-formatted block, such as a paragraph, list, or code fence.",
                "items": {"type": "string"},
            },
            "annotation": {
                "type": "string",
                "description": "A single sentence describing the given response.",
            },
            "predictions": {
                "type": "array",
                "description": "A list of predictive messages used to guide and compose context.",
                "items": {"type": "string"},
            },
            "keywords": {
                "type": "array",
                "description": "A list of no more than three semantic keywords describing the interaction.",
                "items": {"type": "string"},
            },
        },
        "required": ["content", "annotation", "predictions", "keywords"],
        "additionalProperties": False,
    },
    "strict": True,
}


instructions = {
    "type": "json_schema",
    "name": "instructions",
    "schema": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the instructions",
                "default": "",
            },
            "content": {
                "type": "string",
                "description": "Content of the instructions",
                "default": "",
            },
        },
        "additionalProperties": False,
    },
    "strict": True,
}


task = {
    "type": "json_schema",
    "name": "task",
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Name of the task"},
            "instructions": {
                "type": "object",
                "description": "Instructions for the task",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                },
            },
            "activity": {
                "type": "array",
                "description": "List of activities related to this task",
                "items": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "signal": {"type": "object"},
                        "id": {"type": "string"},
                    },
                },
                "default": [],
            },
            "result": {
                "type": ["object", "null"],
                "description": "Result signal of the task",
                "default": None,
            },
            "id": {
                "type": "string",
                "description": "Unique identifier for the task, defaults to a UUID",
            },
        },
        "required": ["name", "instructions"],
        "additionalProperties": False,
    },
    "strict": True,
}


activity = {
    "type": "json_schema",
    "name": "activity",
    "schema": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "ID of the task this activity belongs to",
            },
            "signal": {"type": "object", "description": "A Signal object"},
            "id": {
                "type": "string",
                "description": "Unique identifier for the activity, defaults to a UUID",
            },
        },
        "required": ["task_id", "signal"],
        "additionalProperties": False,
    },
    "strict": True,
}


composition = {
    "type": "json_schema",
    "name": "composition",
    "schema": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name for the given task. It should be relatively short, but memorable and unique as it's used for cross-context communication.",
            },
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
            "prompt": {
                "type": "string",
                "description": "Task-specific instructions for each frame.",
            },
            "construct": {
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


project = {
    "name": "project",
    "type": "json_schema",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of the file or directory.",
        },
        "type": {
            "type": "string",
            "enum": ["file", "directory"],
            "description": "Indicates whether the item is a file or a directory.",
        },
        "contents": {
            "type": "array",
            "description": "Contains files and directories if the item is a directory.",
            "items": {"$ref": "#/$defs/file_system_item"},
        },
    },
    "required": ["name", "type", "contents"],
    "additionalProperties": False,
    "$defs": {
        "file_system_item": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the file or directory.",
                },
                "type": {
                    "type": "string",
                    "enum": ["file", "directory"],
                    "description": "Indicates whether the item is a file or a directory.",
                },
                "contents": {
                    "anyOf": [
                        {"$ref": "#/$defs/folder_content"},
                        {"$ref": "#/$defs/file_content"},
                    ]
                },
            },
            "required": ["name", "type", "contents"],
            "additionalProperties": False,
        },
        "folder_content": {
            "type": "array",
            "description": "Contains files and directories if the item is a directory.",
            "items": {"$ref": "#/$defs/file_system_item"},
        },
        "file_content": {
            "type": "string",
            "description": "The text content of the file.",
        },
    },
    "strict": True,
}


__all__ = (
    input_message,
    output_message,
    instructions,
    task,
    activity,
    composition,
    project,
)
