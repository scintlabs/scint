from fastapi import APIRouter

router = APIRouter()


@router.get("/user/{user_id}")
async def read_agent(user_id: int):
    pass
