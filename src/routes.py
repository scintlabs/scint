from __future__ import annotations

from fastapi import WebSocket, APIRouter
from fastapi.requests import Request

router = APIRouter()


@router.post("/tell")
def tell_endpoint(req: Request):
    pass


@router.post("/ask")
async def ask_endpoint(req: Request):
    pass


@router.get("/system")
async def system_endpoint(req: Request):
    pass


@router.get("/context")
async def context_endpoint(req: Request):
    pass


@router.get("/processes")
async def processes_endpoint(req: Request):
    pass


@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    pass
