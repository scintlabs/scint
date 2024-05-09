from __future__ import annotations
from fastapi import APIRouter, HTTPException
from scint.support.types import List

router = APIRouter()


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


# Mock function to simulate database retrieval
def get_conversation_history(conversation_id: str) -> List[dict]:
    return [{"id": "123", "sender": "user1", "content": "Hello"}]
