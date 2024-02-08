from __future__ import annotations

from fastapi.responses import StreamingResponse

from deltron.data.pipeline import Message
from deltron.coordinator import Coordinator
from deltron.utils import log


coordinator = Coordinator()


async def stream_response(data, function):
    async for response in function(data):
        yield response


async def request(message: Message):
    yield StreamingResponse(
        content=stream_response(data=message, function=coordinator.request),
        media_type="application/json",
    )
