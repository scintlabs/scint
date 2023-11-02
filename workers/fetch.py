from core.config import GPT4
from core.worker import Worker

get_weather = Worker(
    name="get_weather",
    system_init={
        "role": "system",
        "content": "You are a weater retrieval function for Scint, an intelligent assistant.",
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
read_url = Worker(
    name="parse_url",
    system_init={
        "role": "system",
        "content": "You are a website parsing function for Scint, an intelligent assistant.",
        "name": "parse_url",
    },
    function={
        "name": "parse_url",
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
        "function_call": {"name": "parse_url"},
    },
)
search_web = Worker(
    name="search_web",
    system_init={
        "role": "system",
        "content": "You are a web search function for Scint, an intelligent assistant.",
        "name": "search_web",
    },
    function={
        "name": "search_web",
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
        "function_call": {"name": "search_web"},
    },
)
