from __future__ import annotations

import subprocess
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from services.logger import log
from core.coordinator import Coordinator
from core.worker import Worker
from core.message import Message
from core.config import GPT4


coordinator = Coordinator()
app = FastAPI()


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
parse_url = Worker(
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

coordinator.add_worker(get_weather)
coordinator.add_worker(parse_url)


class Response(BaseModel):
    pass


class Request(BaseModel):
    message_data: Dict[str, str]


@app.post("/chat")
async def chat_message(request: Request):
    chat_message = Message("user", "coordinator", request.message_data)

    try:
        chat_response = await coordinator.process_request(chat_message)
        log.info(f"Returning chat response: {chat_response.message_data}")
        return chat_response

    except ValidationError as e:
        log.error(f"Validation Error: {e}")
        return {"error": f"{e}"}

    except Exception as e:
        log.error(f"General Exception: {e}")
        return {"error": f"{e}"}
