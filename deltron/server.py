from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn import Server, Config

from deltron.data.pipeline import DataMessage, SearchMessage, UserMessage
from deltron.endpoints import request
from deltron.utils.logger import log

app = FastAPI()


@app.post("/chat")
async def message_route(message: UserMessage):
    return await request(message=message)


@app.post("/search")
async def upload_route(message: SearchMessage):
    return await request(message=message)


@app.post("/upload")
async def upload_route(message: DataMessage):
    return await request(message=message)


async def server() -> None:
    log.info(f"Starting server ...")
    app.mount("/web", StaticFiles(directory="web"), name="web")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    config = Config(app, host="0.0.0.0", port=8000, reload=True, reload_dirs=["static", "deltron"])
    server = Server(config)
    api = asyncio.create_task(server.serve())
    await asyncio.gather(api)


def start() -> None:
    asyncio.run(server())


if __name__ == "__main__":
    start()
