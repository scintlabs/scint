from __future__ import annotations

from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from scint.message import message_handler, worker_manager
from scint.worker import Worker
from scint.data.prompts import router_init, chatbot_init, status
from scint.data.functions import router, capabilities

router = Worker("router", router_init, status, router)
chatbot = Worker("chatbot", chatbot_init, status, capabilities)
worker_manager.add_worker(chatbot)
worker_manager.add_worker(router)


app = FastAPI()


class Payload(BaseModel):
    worker: str
    message: Dict[str, str]


@app.post("/message")
async def message(payload: Payload):
    try:
        reply = await message_handler(payload.worker, payload.message)
        return reply

    except ValidationError as e:
        return {"error": f"{e}"}

    except Exception as e:
        return {"error": f"{e}"}
