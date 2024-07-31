parse = [
    {
        "name": "file",
        "type": "function",
        "categories": ["parse"],
        "labels": [
            "read file",
            "open file",
            "load file",
            "file",
            "text content",
        ],
        "description": "Reads the content of a file at the given file path. Retrieves the text content of a file for processing or analysis.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to read.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "terminal_commands",
        "type": "function",
        "categories": ["parse"],
        "labels": [
            "terminal",
            "shell",
            "macos",
            "cli",
            "command",
            "command line",
            "subprocess",
        ],
        "description": "Executes shell commands asynchronously and captures the output. Useful for running system commands or scripts from within the application.",
        "parameters": {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "string",
                    "description": "The shell commands to execute.",
                }
            },
            "required": ["commands"],
        },
    },
]
