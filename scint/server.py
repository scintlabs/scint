from __future__ import annotations

import asyncio

import uvicorn
from fastapi import FastAPI

from scint.routers import message_queue, router
from scint.integrations.discord.client import scint_discord
from scint.modules.search import search_controller
from scint.support.utils import env

app = FastAPI()
app.include_router(router)


async def start():
    config = uvicorn.Config(app, host="localhost", port=8000, reload=True)
    server_task = asyncio.create_task(uvicorn.Server(config).serve())
    message_bus_task = asyncio.create_task(message_queue.connect())
    discord_task = asyncio.create_task(scint_discord.start(env("DISCORD_TOKEN")))
    search_task = asyncio.create_task(search_controller.monitor_and_update_indexes())
    await server_task
    await message_bus_task
    await discord_task
    await search_task


def run():
    asyncio.run(start())


if __name__ == "__main__":
    run()
