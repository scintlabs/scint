from __future__ import annotations

from fastapi import APIRouter, FastAPI

from src.runtime.system import System


def create_app(router: APIRouter):
    app = FastAPI()
    app.router = router
    sys = System()
    sys.start()
    return app
