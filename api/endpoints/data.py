from __future__ import annotations
from typing import Dict


from pydantic import BaseModel, ValidationError
from fastapi import FastAPI


from app.services.logging import logger
import app.handlers.message as message


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
        log.logger.error(e.errors())
