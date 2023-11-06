from core.config import GPT4
from core.worker import Worker


get_links = Worker(
    name="get_links",
    system_init={
        "role": "system",
        "content": "You are a web search function for Scint, an intelligent assistant.",
        "name": "get_links",
    },
    function={
        "name": "get_links",
        "description": "Use this function to search the web.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The string to search the web for.",
                },
            },
        },
        "required": ["query"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "get_links"},
    },
)

load_website = Worker(
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
