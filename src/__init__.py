from __future__ import annotations

import asyncio
from uvicorn import Config, Server

from src.bootstrap import create_app
from src.routes import router


async def main():
    app = create_app(router=router)
    cfg = Config(app=app, host="127.0.0.1", port=8000, log_level="info")
    svr = Server(config=cfg)
    tsk = asyncio.create_task(svr.serve())
    _, pnd = await asyncio.wait([tsk], return_when=asyncio.FIRST_COMPLETED)

    for tsk in pnd:
        tsk.cancel()


if __name__ == "__main__":
    asyncio.run(main())
