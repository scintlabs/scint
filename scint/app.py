from __future__ import annotations

import asyncio

import uvicorn
from scint.api.routes import setup_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()
    origins = [
        "https://scint.co",
        "https://assistant.scint.co",
        "http://localhost:8000",
        "http://localhost:8080",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_routes(app)
    return app


async def start():
    server_config = uvicorn.Config(
        app=create_app(), host="0.0.0.0", port=8080, reload=True
    )
    server = uvicorn.Server(server_config)
    api = asyncio.create_task(server.serve())
    await asyncio.gather(api)


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
