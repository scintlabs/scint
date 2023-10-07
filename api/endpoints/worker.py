from fastapi import APIRouter

router = APIRouter()


@router.get("/worker/{worker_id}")
async def read_agent(worker_id: int):
    pass
