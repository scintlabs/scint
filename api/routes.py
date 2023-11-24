from __future__ import annotations

from fastapi import FastAPI

from api.models import Request
from api.endpoints import chat_message, get_context, get_messages


def setup_routes(app: FastAPI):
    @app.post("/chat")
    async def chat_message_route(request: Request):
        return await chat_message(request)

    @app.get("/context")
    def get_context_route():
        return get_context()

    @app.get("/messages")
    def get_messages_route():
        return get_messages()
