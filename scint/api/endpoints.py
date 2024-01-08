from __future__ import annotations

import json
import asyncio

from fastapi.responses import StreamingResponse

from scint.new import persona, respond, context, Message, responder
from scint.api.models import Request
from scint.assistant import assistant
from scint.services.logger import log


async def stream_response(handler):
    try:
        async for response in handler:
            if isinstance(response, Message):
                yield json.dumps(response)

    except Exception as e:
        log.error(f"Endpoint: {e}")


async def chat_message(request: Request):
    message = Message("User", "user", request.content)
    return StreamingResponse(
        stream_response(respond(persona, responder, context, message)),
        media_type="application/json",
    )


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
