from __future__ import annotations

import asyncio
from typing import Any

from fastapi import Body, FastAPI
from pydantic import ValidationError

from base.system.logging import logger
from base.handlers.message import message_handler


app = FastAPI()


@app.post("/chat")
async def chat(request: Any = Body(None)):
    try:
        reply = await message_handler(request)
        return reply

    except ValidationError as e:
        logger.error(e.errors())
