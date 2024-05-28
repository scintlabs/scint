from fastapi import APIRouter, HTTPException, WebSocket

from scint.core.controller import controller
from scint.modules.queue import message_queue
from scint.modules.intelligence import intelligence_controller
from scint.modules.search import search_controller
from scint.modules.storage import storage_controller
from scint.support.types import List

router = APIRouter()

intelligence = intelligence_controller
context = controller
search = search_controller
storage = storage_controller


@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await message_queue.websocket_handler(websocket)


@router.get("/context")
async def current_context():
    return await controller.current_context()


@router.get("/conversations/{conversation_id}", response_model=List[dict])
async def fetch_conversation(conversation_id: str):
    messages = get_conversation_history(conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages


def gather_metadata(metadata):
    result = {"name": metadata.name, "children": [], "data": []}
    for child in metadata.children:
        result["children"].append(gather_metadata(child))
    for data in metadata.get("_data"):
        if data:
            result["data"].append({"name": data})
    return result


def get_conversation_history(conversation_id: str) -> List[dict]:
    return [{"id": "123", "sender": "user1", "content": "Hello"}]
