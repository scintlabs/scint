import uvicorn
from fastapi import FastAPI

from scint.server.routes import router

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("scint.__main__:app", port=8000, reload=True)
