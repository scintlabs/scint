from __future__ import annotations
from fastapi import FastAPI
from scint.api import message

app = FastAPI()
app.include_router(message.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, reload=True, host="localhost", port=8000)
