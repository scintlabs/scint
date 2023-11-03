from core.config import GPT4

generate_text = {
    "name": "generate_text",
    "system_init": {
        "role": "system",
        "content": "You are a factory function for an artificial intelligence system. For every message, generate text according to the specification.",
        "name": "generate_text",
    },
    "function": {
        "name": "generate_text",
        "description": "Use this function to generate text content.",
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
        "temperature": 1.8,
        "top_p": 0.4,
        "presence_penalty": 0.3,
        "frequency_penalty": 0.3,
        "function_call": {"name": "generate_text"},
    },
}

generate_code = {
    "name": "generate_code",
    "system_init": {
        "role": "system",
        "content": "You are a factory function for an artificial intelligence system. For every message, generate code and ONLY code according to the specification.",
        "name": "generate_code",
    },
    "function": {
        "name": "generate_code",
        "description": "Use this function to generate code.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The generated code.",
                },
            },
        },
        "required": ["code"],
    },
    "config": {
        "model": GPT4,
        "temperature": 1.2,
        "top_p": 0.5,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "generate_code"},
    },
}
