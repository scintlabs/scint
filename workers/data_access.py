from core.worker import Worker
from core.config import GPT4

query_database = {
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

get_weather = Worker(
    name="get_weather",
    system_init={
        "role": "system",
        "content": "You are a weather retrieval function for Scint, an intelligent assistant.",
        "name": "get_weather",
    },
    function={
        "name": "get_weather",
        "description": "Use this function to get weather data for the specified city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name.",
                },
            },
        },
        "required": ["city"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "get_weather"},
    },
)
