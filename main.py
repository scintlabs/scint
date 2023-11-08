from __future__ import annotations

import json
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ValidationError

from services.logger import log
from core.coordinator import Coordinator
from workers.web_browsing import search_web, load_website
from workers.data_access import query_database, get_weather
from workers.file_operations import file_operations

coordinator = Coordinator()
coordinator.add_workers(
    file_operations,
    get_weather,
    search_web,
    load_website,
)
app = FastAPI()


class Response(BaseModel):
    pass


class Request(BaseModel):
    message: Dict[str, str]


async def stream_response(request_message):
    try:
        async for chunk in coordinator.process_request(request_message):
            yield json.dumps(chunk) + "\n"

    except ValidationError as e:
        log.error(f"Validation Error: {e}")

    except Exception as e:
        log.error(f"General Exception: {e}")


@app.post("/chat")
async def chat_message(request: Request):
    return StreamingResponse(
        stream_response(request.message), media_type="application/json"
    )


@app.get("/context")
def get_context():
    try:
        return json.dumps(coordinator.context_controller.get_context())

    except Exception as e:
        log.error(f"Error retrieving context: {e}")


@app.get("/messages")
def get_context():
    try:
        return json.dumps(coordinator.context_controller.get_messages())

    except Exception as e:
        log.error(f"Error retrieving context: {e}")
