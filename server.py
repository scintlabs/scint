import asyncio

from fastapi import FastAPI, WebSocket, HTTPException, Depends

from base.definitions.types import UserRequest
from base.cli import run_cli
from base.state import StateManager
from util.logging import logger


app = FastAPI()


@app.post("/chat/")
async def chat_endpoint(payload: UserRequest):
    # Integrate with Scint's message handling
    response = {}  # Get response from Scint
    return {"response": response}


if __name__ == "__main__":
    asyncio.run(run_cli())
