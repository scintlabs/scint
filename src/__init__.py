from __future__ import annotations

import asyncio
import uvicorn
from fastapi import FastAPI

from src.bootstrap import bootstrap


async def main():
    await bootstrap()
    server = uvicorn.Server(
        uvicorn.Config(app=FastAPI(), host="127.0.0.1", port=8000, log_level="info")
    )
    server_task = asyncio.create_task(server.serve())
    done, pending = await asyncio.wait(
        [server_task], return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
