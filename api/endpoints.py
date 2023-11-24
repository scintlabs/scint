from __future__ import annotations

import json
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from api.models import Request
from services.logger import log
from app_setup import persona


async def stream_chat_response(request_message):
    try:
        async for chunk in persona.process_request(request_message):
            yield json.dumps(chunk) + "\n"

    except ValidationError as e:
        log.error(f"Validation Error: {e}")

    except Exception as e:
        log.error(f"General Exception: {e}")


async def chat_message(request: Request):
    return StreamingResponse(
        stream_chat_response(request.message),
        media_type="application/json",
    )


def get_context():
    try:
        return json.dumps(persona.context_controller.get_context())

    except Exception as e:
        log.error(f"Error retrieving context: {e}")


def get_messages():
    try:
        return json.dumps(persona.context_controller.get_messages())

    except Exception as e:
        log.error(f"Error retrieving context: {e}")
