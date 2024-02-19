from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn import Config, Server

from scint.components.models import SystemMessage, UserMessage
from scint.endpoints import chat_endpoint, process_mapping_endpoint
from scint.utils.logger import log

app = FastAPI()


@app.post("/processes/chat")
async def chat(message: UserMessage):
    return await chat_endpoint(message=message)


@app.post("/processes/mapping")
async def process_mapping(process_name):
    return await process_mapping_endpoint(process_name)


async def server() -> None:
    log.info(f"Starting server.")
    dirs = ["scint", "web"]
    origins = ["http://localhost:8000"]
    methods = ["*"]
    headers = ["*"]
    app.mount("/web", StaticFiles(directory="web"), name="web")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=methods,
        allow_headers=headers,
    )
    config = Config(app, host="localhost", port=8000, reload=True, reload_dirs=dirs)
    server = Server(config)
    api = asyncio.create_task(server.serve())
    await asyncio.gather(api)


def start() -> None:
    asyncio.run(server())


if __name__ == "__main__":
    start()
