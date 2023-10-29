from __future__ import annotations

from fastapi import FastAPI

from api.models import Request

app = FastAPI()


@app.post("/chat")
async def chat_message(request: Request):
    pass
    # try:
    #     chat_response = await coordinator.process_request(request.message)
    #     log.info(f"Returning chat response: {chat_response}")  # type: ignore
    #     return chat_response

    # except ValidationError as e:
    #     log.error(f"Validation Error: {e}")
    #     return {"error": f"{e}"}

    # except Exception as e:
    #     log.error(f"General Exception: {e}")
    #     return {"error": f"{e}"}
