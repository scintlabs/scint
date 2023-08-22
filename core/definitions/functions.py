google_search = {
    "name": "google_search",
    "description": "Use this function to run a Google search for the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search string to use.",
            },
        },
        "required": ["query"],
    },
}


generate_code = {
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
