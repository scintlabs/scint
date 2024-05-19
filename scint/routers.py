from __future__ import annotations

from fastapi import APIRouter, HTTPException, WebSocket

from scint.support.types import List
from scint.controllers.queue import message_bus
from scint.controllers.context import context_controller
from scint.controllers.intelligence import intelligence_controller
from scint.controllers.search import search_controller
from scint.controllers.storage import storage_controller


context = context_controller
intelligence = intelligence_controller
search = search_controller
storage = storage_controller


router = APIRouter()


@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """
    """
    await message_bus.websocket_handler(websocket)


@router.get("/context")
async def get_context():
    """
    """
    return context_controller.get_global_context()


@router.get("/conversations/{conversation_id}", response_model=List[dict])
async def fetch_conversation(conversation_id: str):
    """
    """
    messages = get_conversation_history(conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages


def gather_metadata(metadata):
    """
    """
    result = {"name": metadata.name, "children": [], "data": []}
    for child in metadata.children:
        result["children"].append(gather_metadata(child))
    for data in metadata.get("_data"):
        if data:
            result["data"].append({"name": data})
    return result


def get_conversation_history(conversation_id: str) -> List[dict]:
    """
    """
    return [{"id": "123", "sender": "user1", "content": "Hello"}]
