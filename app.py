from __future__ import annotations

import asyncio
import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.routes import setup_routes

app = FastAPI()
setup_routes(app)


async def start():
    server_config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(server_config)
    api = asyncio.create_task(server.serve())
    await asyncio.gather(api)


if __name__ == "__main__":
    asyncio.run(start())
