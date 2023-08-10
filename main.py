import sys, signal, subprocess, asyncio
import core.prompt as prompt
import core.definitions.types as types
from core.prompt import Prompt, meta_prompts
from core.generator import generate
from core.completer import complete
from fastapi import FastAPI
from typing import Union

validate = meta_prompts["validate"]
refactor = meta_prompts["refactor"]
sort = meta_prompts["sort"]
recurse = meta_prompts["recurse"]
diverge = meta_prompts["diverge"]

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
