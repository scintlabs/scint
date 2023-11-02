from __future__ import annotations

import json
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ValidationError

from services.logger import log
from core.coordinator import Coordinator
from workers.fetch import search_web, read_url, get_weather


coordinator = Coordinator()
coordinator.add_workers(search_web, read_url, get_weather)

app = FastAPI()


class Response(BaseModel):
    pass


class Request(BaseModel):
    message: Dict[str, str]


async def stream_response(request_message):
    try:
        async for chunk in coordinator.generate_response(request_message):
            yield json.dumps(chunk) + "\n"

    except ValidationError as e:
        log.error(f"Validation Error: {e}")
        yield json.dumps({"error": f"{e}"}) + "\n"

    except Exception as e:
        log.error(f"General Exception: {e}")
        yield json.dumps({"error": f"{e}"}) + "\n"


@app.post("/chat")
async def chat_message(request: Request):
    return StreamingResponse(
        stream_response(request.message), media_type="application/json"
    )
