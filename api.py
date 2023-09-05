import asyncio

from fastapi import FastAPI, WebSocket, HTTPException, Depends, Body

from base.definitions.types import Message
from base.chat import send_message
from base.cli import run_cli
from util.logging import logger


app = FastAPI()


@app.post("/assistant/")
async def assistant_chat(message: Message):
    try:
        response = await send_message(message)
        return {"response": response}
    except Exception as e:
        logger.exception(f"Error communicating with the Scint API: {e}\n")


if __name__ == "__api__":
    asyncio.run(app())
