from __future__ import annotations

from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from services.logger import log
from core.coordinator import Coordinator
from core.worker import Worker
from core.message import Message
from core.prompts import chat_init
from core.functions import base_functions

app = FastAPI()

chat = Worker("chat", chat_init, base_functions)
coordinator = Coordinator()
coordinator.add_worker(chat)


class Response(BaseModel):
    pass


class Request(BaseModel):
    worker: str
    message: Dict[str, str]


@app.post("/chat")
async def chat_message(request: Request):
    chat_message = Message("user", request.worker, request.message)

    try:
        chat_response = await coordinator.process_request(chat_message)
        log.info(f"Returning chat response: {chat_response}")
        return chat_response

    except ValidationError as e:
        log.error(f"Validation Error: {e}")
        return {"error": f"{e}"}

    except Exception as e:
        log.error(f"General Exception: {e}")
        return {"error": f"{e}"}
