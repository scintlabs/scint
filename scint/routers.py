from fastapi import APIRouter, HTTPException, WebSocket

from scint.core.controller import controller
from scint.modules.queue import message_queue
from scint.support.types import List

router = APIRouter()


@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await message_queue.websocket_handler(websocket)


@router.get("/context")
async def get_active_contexts():
    if len(controller.contexts) > 0:
        context_object = {}
        for active_context in controller.contexts:
            prompts = controller.extract_context(active_context.prompts)
            messages = controller.extract_context(active_context.messages)
            context_object[active_context.name] = {
                "description": active_context.description,
                "messages": prompts + messages,
            }
        return context_object


@router.get("/threads")
async def get_threads():
    threads_object = {}
    for thread in controller.threads.children:
        threads_object[thread.name] = {
            "description": thread.description,
            "messages": thread.messages.metadata,
        }
    return threads_object


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
