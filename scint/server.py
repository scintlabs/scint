from __future__ import annotations

import asyncio
from fastapi import FastAPI
import uvicorn
from scint.routers import message_bus, router

app = FastAPI()
app.include_router(router)


async def start():
    config = uvicorn.Config(app, host="localhost", port=8000, reload=True)
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())
    message_bus_task = asyncio.create_task(message_bus.connect())
    await server_task
    await message_bus_task


def run():
    asyncio.run(start())


if __name__ == "__main__":
    run()
