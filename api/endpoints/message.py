from __future__ import annotations
from typing import Any, Dict


from app.services.logging import logger
from app.handlers import message, data
from pydantic import BaseModel
from fastapi import Body, FastAPI
from pydantic import ValidationError


app = FastAPI()
endpoint = "http://localhost:8000/chat"


class Payload(BaseModel):
    agent: str
    message: Dict[str, str]


@app.post("/chat")
async def chat(payload: Payload):
    try:
        reply = await message.message_handler(payload.agent, payload.message)
        return reply

    except ValidationError as e:
        logger.error(e.errors())
