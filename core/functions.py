functions = [
    {
        "name": "generate_content",
        "description": "Use this function to write text content, either prose or code, and save it to the active buffer.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Code or text content you generate on the user's behalf.",
                },
            },
            "required": ["content"],
        },
    }
]
