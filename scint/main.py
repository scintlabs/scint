from __future__ import annotations
from typing import Dict
import asyncio

from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import ValidationError

from services.logging import logger
from handlers import message
from services.cli import run_cli


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
