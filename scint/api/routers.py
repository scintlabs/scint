from fastapi import APIRouter, HTTPException, WebSocket

from scint.messaging.queue import message_queue
from scint.support.types import List

router = APIRouter()


@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await message_queue.websocket_handler(websocket)
