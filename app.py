import asyncio

from fastapi import FastAPI, WebSocket, HTTPException, Depends

from core.definitions.types import ChatMessage, Command, StateMessage, Observation
from core.cli import run_cli
from core.observer import Observer
from core.state import State


app = FastAPI()


@app.post("/chat/")
async def chat_endpoint(payload: ChatMessage):
    # Integrate with Scint's message handling
    response = {}  # Get response from Scint
    return {"response": response}


@app.post("/command/")
async def command_endpoint(payload: Command):
    # Integrate with Scint's command execution
    result = {}  # Get result from executing the command
    return {"result": result}


@app.get("/prompts/")
async def get_prompts():
    # Fetch available prompts from Scint
    prompts = []  # List of available prompts
    return {"prompts": prompts}


@app.get("/state/")
async def get_state():
    # Fetch Scint's current state
    state = ""  # Get current state
    return {"state": state}


@app.post("/state/")
async def set_state(payload: StateMessage):
    # Set or update Scint's state
    # Update state in Scint
    return {"state": payload.state}


@app.get("/observe/")
async def get_observations():
    # Fetch Scint's current observations
    observations = {}  # Get current observations
    return {"observations": observations}


@app.post("/observe/")
async def set_observations(payload: Observation):
    # Set specific observation parameters in Scint
    # Update observations in Scint
    return {"observation": payload.observe}


@app.websocket("/ws/chat/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = {}
        # await websocket.send_text(response)


if __name__ == "__main__":
    asyncio.run(run_cli())
