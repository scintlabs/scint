from core.config import GPT4


access_database = {
    "name": "access_database",
    "system_init": {
        "role": "system",
        "content": "You are the database interface for Scint, a state-of-the-art intelligent assistant.",
        "name": "access_database",
    },
    "function": {
        "name": "access_database",
        "description": "Use this function to search the Scint database.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The generated text content.",
                },
            },
        },
        "required": ["content_type", "content"],
    },
    "config": {
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "access_database"},
    },
}
