from __future__ import annotations
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import ValidationError

from api.models.payload import Payload


app = APIRouter()


@app.post("/message")
async def message(payload: Payload):
    try:
        reply = await message.message_handler(payload)
        return reply

    except ValidationError as e:
        return {"error": f"{e}"}

    except Exception as e:
        return {"error": f"{e}"}
