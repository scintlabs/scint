build = {
    "name": "function",
    "type": "function",
    "description": "Use this function to specify and create a new function within the system.",
    "categories": ["build"],
    "labels": [
        "Create a new system function.",
        "New internal function.",
        "Develop a new function",
    ],
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The function's name. Use a verbose name that clearly describes the function's purpose.",
            },
            "description": {
                "type": "string",
                "description": "A description of the function, explaining succinctly but in detail what the function does and when and how to use it.",
            },
            "parameters": {
                "type": "object",
                "description": "The function's parameters. Return an object containing key value pairs for each parameter. The key should be the parameter name, and the value should be an object containing keys and values for parameter type, parameter description, any default values, and whether the parameter is required.",
            },
            "source": {
                "type": "object",
                "properties": {
                    "definition": {
                        "type": "string",
                        "description": "The function's definition line, as written in the source. All system functions must be asynchronous generators.",
                    },
                    "body": {
                        "type": "string",
                        "description": "The main function body.",
                    },
                    "yields": {
                        "type": "string",
                        "description": "The yield statement, as it should appear in the source code. Remember that all return values must be within a SystemMessage pydantic class, assigned to the 'content' parameter.",
                    },
                },
            },
        },
        "required": ["name", "description", "parameters", "required"],
    },
}
