from core.config import GPT4


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
