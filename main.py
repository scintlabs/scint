from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from services.logger import log
from core.coordinator import Coordinator
from core.worker import Worker
from core.config import GPT4


coordinator = Coordinator()
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
generate_text = Worker(
    name="generate_text",
    system_init={
        "role": "system",
        "content": "You are a content generating function for Scint, an intelligent assistant.",
        "name": "generate_text",
    },
    function={
        "name": "generate_text",
        "description": "Use this function to generate content.",
        "parameters": {
            "type": "object",
            "properties": {
                "content_type": {
                    "type": "string",
                    "description": "The type of content being generated.",
                },
                "content": {
                    "type": "string",
                    "description": "The generated content.",
                },
            },
        },
        "required": ["content_type", "content"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "generate_text"},
    },
)
crud_file = Worker(
    name="crud_file",
    system_init={
        "role": "system",
        "content": "You are a CRUD file function for Scint, an intelligent assistant.",
        "name": "crud_file",
    },
    function={
        "name": "crud_file",
        "description": "Use this function to perform CRUD operations on a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The complete filepath to the file.",
                },
                "operation": {
                    "type": "string",
                    "description": "The operation to run on the specified file.",
                    "enum": ["create", "read", "update", "delete"],
                },
                "content": {
                    "type": "string",
                    "description": "The content to create or update files with.",
                },
            },
        },
        "required": ["filename", "operation"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "crud_file"},
    },
)

control_flows: Dict[str, List[Worker]] = {
    "create_blog_post": [crud_file, search_web, generate_text, crud_file],
    "browse_web": [search_web, read_url],
}

coordinator.add_workers(search_web, read_url, generate_text, crud_file)
coordinator.add_control_flows(control_flows)

app = FastAPI()


class Response(BaseModel):
    pass


class Request(BaseModel):
    message: Dict[str, str]


@app.post("/chat")
async def chat_message(request: Request):
    try:
        chat_response = await coordinator.process_request(request.message)
        log.info(f"Returning chat response: {chat_response}")  # type: ignore
        return chat_response

    except ValidationError as e:
        log.error(f"Validation Error: {e}")
        return {"error": f"{e}"}

    except Exception as e:
        log.error(f"General Exception: {e}")
        return {"error": f"{e}"}
