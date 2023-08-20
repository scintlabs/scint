generate_code = [
    {
        "name": "generate_code",
        "description": "Use this function to write and test Python code. Files are created and executed in a secure environment.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to write and execute. You may write files and folders to create complex projects using Python.",
                },
            },
            "required": ["code"],
        },
    }
]
