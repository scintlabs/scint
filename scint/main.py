from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uvicorn import Server, Config

from scint.core.coordinator import Coordinator
from scint.core.messages import Request, UserMessage
from scint.services.logger import log

coordinator = Coordinator()
app = FastAPI()


@app.get("/")
def main_route(request: Request):
    templates = Jinja2Templates(directory="templates")
    response = {"name": "index.html", "content": {"request": request}}

    try:
        return templates.TemplateResponse(**response)

    except Exception as e:
        log.error(f"Endpoint: {e}")


@app.post("/web_search")
async def web_search(request: Request):
    content = request.content
    message = UserMessage(content, __name__)
    return StreamingResponse(stream_response(message), media_type="application/json")


async def stream_response(message):
    try:
        async for response in coordinator.process_request(message):
            if isinstance(response, UserMessage):
                yield json.loads(response.data_dump())

    except Exception as e:
        log.error(f"Endpoint: {e}")


async def fastapi_server():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/templates", StaticFiles(directory="templates"), name="templates")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    config = Config(app, host="localhost", port=8000, reload=True)
    server = Server(config)
    api = asyncio.create_task(server.serve())
    await asyncio.gather(api)


def main():
    asyncio.run(fastapi_server())


if __name__ == "__main__":
    main()
