from core.config import GPT4
from core.worker import Worker

fetch_weather = Worker(
    name="fetch_weather",
    system_init={
        "role": "system",
        "content": "You are a weather retrieval function for Scint, an intelligent assistant.",
        "name": "fetch_weather",
    },
    function={
        "name": "fetch_weather",
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
        "function_call": {"name": "fetch_weather"},
    },
)
fetch_files = Worker(
    name="fetch_files",
    system_init={
        "role": "system",
        "content": "You are a file retrieval function for Scint, an intelligent assistant.",
        "name": "fetch_files",
    },
    function={
        "name": "fetch_files",
        "description": "Use this function to access a file or directory within the Scint system.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to access.",
                },
                "filename": {
                    "type": "string",
                    "description": "The filename to access. If no filename is given, the function returns a list of files in the given directory.",
                },
            },
        },
        "required": ["directory"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "fetch_files"},
    },
)
fetch_website = Worker(
    name="fetch_website",
    system_init={
        "role": "system",
        "content": "You are a website parsing function for Scint, an intelligent assistant.",
        "name": "fetch_website",
    },
    function={
        "name": "fetch_website",
        "description": "Use this function to get website data from the specified URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the website to parse.",
                },
            },
        },
        "required": ["url"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "fetch_website"},
    },
)
