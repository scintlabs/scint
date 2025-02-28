from fastapi import APIRouter, HTTPException

from scint.api import ScintInterface
from scint.lib.switch import Request


interface = ScintInterface()
router = APIRouter()


@router.post("/messages")
async def messages_endpoint(req: Request):
    try:
        res = await interface.messages(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tasks")
async def tasks_endpoint(req: Request):
    try:
        res = await interface.tasks(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/library")
async def library_endpoint(req: Request):
    try:
        res = await interface.library(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/settings")
async def settings_endpoint(req: Request):
    try:
        res = await interface.settings(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/find")
async def find_endpoint(req: Request):
    try:
        res = await interface.find(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
