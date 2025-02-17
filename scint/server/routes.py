from fastapi import APIRouter, HTTPException

from scint.server.models import Request
from scint.client.client import ScintClient


router = APIRouter()
client = ScintClient()


@router.post("/message")
async def message(req: Request):
    try:
        res = await client.input(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tasks")
async def tasks(req: Request):
    try:
        res = await client.tasks(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/processes")
async def processes(req: Request):
    try:
        res = await client.processes(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/library")
async def storage(req: Request):
    try:
        res = await client.library(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search")
async def search(req: Request):
    try:
        res = await client.library(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
