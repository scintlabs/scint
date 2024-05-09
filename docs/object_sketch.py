object = {
    "name": "name",
    "intelligence": "intelligence",
    "directives": [
        {
            "type": "container",
            "name": "directives",
            "description": "System messages.",
            "properties": {
                "directive": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "You are a...",
                        },
                    },
                },
            },
        },
    ],
    "messages": [
        {
            "role": "system",
            "content": "Welcome to the system. How can I help you today?",
        },
        {
            "role": "user",
            "content": "I would like to search for something on the web.",
        },
        {
            "role": "system",
            "content": "Sure thing. What would you like to search for?",
        },
        {
            "role": "user",
            "content": "I would like to search for something something.",
        },
        {
            "role": "system",
            "content": "I will search for something something on the web.",
        },
        {
            "role": "system",
            "content": "Here are the search results for something something.",
        },
        {
            "role": "system",
            "content": "Would you like to search for something else?",
        },
        {
            "role": "user",
            "content": "No, thank you.",
        },
        {
            "role": "system",
            "content": "Thank you for using the system. Have a great day!",
        },
    ],
    "research": {
        "type": "interface",
        "description": "A research interface for gathering highly relevant, contextualized data and information from across the web, local documets, application history, and more.",
        "properties": {
            "projects": {
                "type": "container",
                "description": "Research projects.",
                "properties": {
                    "project": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the project.",
                            },
                            "journal": {
                                "type": "string",
                                "description": "Parameters used, progress made, and the results.",
                            },
                        },
                    },
                },
            },
            "new": {
                "type": "object",
                "description": "Start a new research project.",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the research project.",
                    },
                    "keywords": {
                        "type": "string",
                        "description": "Keywords to use.",
                    },
                    "sources": {
                        "type": "string",
                        "description": "The list of sources to to begin searching.",
                        "enum": ["web", "files", "system", "history"],
                    },
                    "strategies": {
                        "type": "string",
                        "description": "The search strategies to use.",
                        "enum": ["exact", "fuzzy", "breadth-first", "depth-first"],
                    },
                },
            },
        },
    },
    "system": {
        "type": "interface",
        "name": "system",
        "description": "Contextual information and for maintaining system integrity.",
        "properties": {
            "datetime": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The current date.",
                    },
                    "time": {
                        "type": "string",
                        "description": "The current time.",
                    },
                },
            },
            "events": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The event ID.",
                    },
                    "name": {
                        "type": "string",
                        "description": "The event name.",
                    },
                    "description": {
                        "type": "string",
                        "description": "The event description.",
                    },
                    "priority": {
                        "type": "string",
                        "description": "The event priority.",
                    },
                },
            },
        },
    },
    "functions": [
        {
            "name": "use_terminal",
            "description": "Use this function to run UNIX terminal commands from a macOS terminal with full sudo privileges.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The UNIX terminal command to execute.",
                    },
                },
                "required": "commandsX",
            },
            "attributes": {
                "type": "object",
                "properties": {
                    "process": {
                        "type": "string",
                        "content": "await asyncio.create_subprocess_shell(\n            commands,\n            stdout=asyncio.subprocess.PIPE,\n            stderr=asyncio.subprocess.PIPE,\n        )",
                    },
                    "stdout": {
                        "type": "string",
                        "content": "await process.communicate()",
                    },
                    "output": {
                        "type": "string",
                        "description": "stdout.decode().strip() if stdout else ''",
                    },
                    "errors": {
                        "type": "string",
                        "description": "stderr.decode().strip() if stderr else ''",
                    },
                    "full_output": {
                        "type": "string",
                        "description": "output + '\\n' + errors if errors else output",
                    },
                    "yields": "Message(role='system', content=full_output)",
                },
            },
        },
        {
            "name": "send_notification",
            "description": "Use this function to send notifications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "notification": {
                        "type": "string",
                        "description": "The notification to send.",
                    },
                },
                "required": "notification",
            },
        },
    ],
}
