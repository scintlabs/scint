functions = [
    {
        "name": "write_code",
        "description": "Use this function to write code and save it to a destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Your source code.",
                },
                "filetype": {
                    "type": "string",
                    "description": "The file format of your code.",
                },
                "destination": {
                    "type": "string",
                    "description": "Where to save your code.",
                },
            },
            "required": ["code", "filetype", "destination"],
        },
    }
]
