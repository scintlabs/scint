from __future__ import annotations

from fastapi import FastAPI

from api.models import Request
from core.message import Message

app = FastAPI()


@app.post("/chat")
async def chat_message(request: Request):
    chat_message = Message("user", request.worker, request.message)
