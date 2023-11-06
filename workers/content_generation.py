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
