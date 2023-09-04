LOCATOR = {
    "name": "locator",
    "description": "Initialize the locator state to search for files, data, or information required for user requests or tasks.",
    "parameters": {
        "type": "object",
        "properties": {
            "search_query": {
                "type": "string",
                "description": "Use this parameter to inform the user that you're initiating a search.",
            },
            "success_definition": {
                "type": "string",
                "description": "Based on the given query, provide a threshold of a successful search result.",
            },
            "user_response": {
                "type": "string",
                "description": "Inform the user that you're beginning the search process.",
            },
        },
        "required": [
            "search_query",
            "define_success",
            "user_response",
        ],
    },
}

PROCESSOR = {
    "name": "processor",
    "description": "Initialize the processor state to evaluate, parse, analyze, or categorize data, such as evaluating a codebase, summarizing a book, or generating embeddings.",
    "parameters": {
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "A description of the assigned task.",
            },
            "data": {
                "type": "string",
                "description": "The data required to complete the task. Valid strings can be a filesystem link or string data, such as Python code to execute.",
            },
            "define_success": {
                "type": "string",
                "description": "Based on the given query, provide a threshold of a successful search result.",
            },
            "user_response": {
                "type": "string",
                "description": "Use this parameter to inform the user that you started processing data.",
            },
        },
        "required": ["user_response", "define_success"],
    },
}

TRANSFORMER = {
    "name": "transformer",
    "description": "Initialize the transformer state to orchestrate data pipelines and generate code and content for complex tasks and large projects.",
    "parameters": {
        "type": "object",
        "properties": {
            "config": {
                "type": "string",
                "description": "Provide the name of the configuration file for generating content.",
            },
            "define_success": {
                "type": "string",
                "description": "Based on the given query, provide a threshold of a successful search result.",
            },
            "user_response": {
                "type": "string",
                "description": "Let the user know you're starting the transformer process.",
            },
        },
        "required": [
            "define_success",
            "context_id",
            "user_response",
        ],
    },
}
