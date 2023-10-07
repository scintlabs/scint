from __future__ import annotations
import asyncio
import aiohttp
from typing import Any, Dict

from pydantic import BaseModel
from fastapi import Body, FastAPI
from pydantic import ValidationError
from app.workers.worker import Worker


from app.services.logging import logger
from app.handlers.message import message_handler


app = FastAPI()
endpoint = "http://localhost:8000/chat"


class Agent(BaseModel, Worker):
    name: str


class Payload(BaseModel):
    agent: str
    message: Dict[str, str]


@app.post("/chat")
async def chat(payload: Payload):
    try:
        reply = await message_handler(payload.agent, payload.message)
        return reply

    except ValidationError as e:
        logger.error(e.errors())
