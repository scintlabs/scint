import asyncio

from fastapi import Body, Depends, FastAPI, HTTPException, WebSocket

app = FastAPI()


# @app.post("/assistant/")
# async def assistant_chat(message: Message):
#     try:
#         response = await send_message(message)
#         return {"response": response}
#     except Exception as e:
#         logger.exception(f"Error communicating with the Scint API: {e}\n")


# if __name__ == "__api__":
#     asyncio.run(app())
