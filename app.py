from __future__ import annotations

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import setup_routes

app = FastAPI()
setup_routes(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def start():
    server_config = uvicorn.Config(app=app, host="0.0.0.0", port=8080, reload=True)
    server = uvicorn.Server(server_config)
    api = asyncio.create_task(server.serve())
    await asyncio.gather(api)


if __name__ == "__main__":
    asyncio.run(start())
