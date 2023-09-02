response = {
    "name": "response",
    "description": "Use this function to response to and classify user messages.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to respond to the user with.",
            },
            "keywords": {
                "type": "string",
                "description": "A list of keywords to classify the message for future search and retrieval.",
            },
            "conversation": {
                "type": "boolean",
                "description": "If the message is a continuation of the previous conversation, return true, otherwise return false.",
            },
        },
        "required": ["message", "keywords", "conversation"],
    },
}

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

generate_prose = {
    "name": "generate_code",
    "description": "Use this function to write and test Python code. Files are created in a secure environment.",
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
