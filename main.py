from __future__ import annotations
from typing import Dict

from pydantic import BaseModel, ValidationError
from fastapi import FastAPI

from scint.handlers.message import message_handler


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


@app.post("/function_call")
async def function_call(payload: Payload):
    try:
        reply = await message_handler(payload.worker, payload.message)
        return reply

    except ValidationError as e:
        return {"error": f"{e}"}

    except Exception as e:
        return {"error": f"{e}"}
