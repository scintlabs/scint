from __future__ import annotations

import asyncio

import uvicorn

from src.boot.container import build_container
from src.boot.console import Console


async def main():
    container = await build_container()
    console_task = asyncio.create_task(Console(broker=container.broker).start())
    uvi = uvicorn.Config(container.base, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(uvi)
    server_task = asyncio.create_task(server.serve())

    done, pending = await asyncio.wait(
        [console_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
