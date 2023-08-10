import sys, signal, subprocess, asyncio
import core.prompt
import core.definitions.types as types
from core.prompt import Prompt, meta_prompts
from core.generator import generate
from fastapi import FastAPI
from typing import Union


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
