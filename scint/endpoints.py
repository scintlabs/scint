from __future__ import annotations

from fastapi.responses import StreamingResponse

from scint.components.models import Message
from scint.main import Main

main = Main()


async def stream_response(function):
    async for response in function:
        yield response.model_dump_json(include=["id", "sender", "content"]) + "\n"


async def chat_endpoint(message: Message):
    return StreamingResponse(
        content=stream_response(function=main.execute(message=message)),
        media_type="application/json",
    )


async def process_mapping_endpoint(process_name: str, recurse=True):
    return main.build_execution_map()
