from __future__ import annotations

import asyncio

import uvicorn
from fastapi import FastAPI

from scint.services.search import search_controller
from scint.api.routers import message_queue, router
from scint.support.utils import env

app = FastAPI()
app.include_router(router)


async def start():
    config = uvicorn.Config(app, host="localhost", port=8000, reload=True)
    server = asyncio.create_task(uvicorn.Server(config).serve())
    messages = asyncio.create_task(message_queue.connect())
    search = asyncio.create_task(search_controller.monitor_indexes())
    await server
    await messages
    await search


def run():
    asyncio.run(start())


if __name__ == "__main__":
    run()
