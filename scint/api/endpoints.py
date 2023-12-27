from __future__ import annotations

import json

from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from scint.api.models import Request
from scint.assistant import assistant
from scint.core.context import Message
from scint.services.logger import log


async def stream_response(request: Message):
    try:
        async for response in assistant.generate_response(request):
            if isinstance(response, Message):
                yield json.dumps(response.data_dump())

    except ValidationError as e:
        log.error(f"Endpoint: {e}")

    except Exception as e:
        log.error(f"Endpoint: {e}")


async def chat_message(request: Request):
    message = Message("user", request.content, "User")
    return StreamingResponse(stream_response(message), media_type="application/json")


def get_context():
    try:
        context = assistant.memory_manager.get_context()
        return json.dumps(context)

    except Exception as e:
        log.error(f"Error retrieving context: {e}")
        return json.dumps({"error": str(e)})


def get_messages():
    try:
        messages = assistant.memory_manager.get_messages()
        return [message for message in messages]

    except Exception as e:
        log.error(f"Error retrieving messages: {e}")
        return json.dumps({"error": str(e)})
