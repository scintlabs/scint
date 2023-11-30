from __future__ import annotations

import json

from api.models import Request
from app_setup import persona
from core.memory import Message
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from services.logger import log


async def stream_chat_response(request_message: Request):
    request_message = Message(**request_message)
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
        context = persona.context.build_context()
        return json.dumps(context)

    except Exception as e:
        log.error(f"Error retrieving context: {e}")
        return json.dumps({"error": str(e)})


def get_messages():
    try:
        messages = persona.context.get_messages()
        return json.dumps([message.data_dump() for message in messages])

    except Exception as e:
        log.error(f"Error retrieving messages: {e}")
        return json.dumps({"error": str(e)})
