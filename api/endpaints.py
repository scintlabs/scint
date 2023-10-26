from __future__ import annotations

from fastapi import FastAPI

from api.models import Payload
from scint.message import Message

app = FastAPI()


@app.post("/chat")
async def chat_message(payload: Payload):
    chat_message = Message("user", payload.worker, payload.message)
