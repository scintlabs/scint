import os, aiofiles
from fastapi import FastAPI, UploadFile
from typing import Dict, Optional
from pydantic import BaseModel
from pathlib import Path
from core.data.environment import FILESTORE


app = FastAPI()


class File(BaseModel):
    name: str
    content: str
    filepath: str


file = File


@app.get("/")
def read_root():
    return {"message": "You've discovered the scintessence."}


@app.get("/files/")
async def read_file(name: str, filepath: str = ""):
    if filepath:
        filepath = os.path.join(FILESTORE, filepath, name)
    else:
        filepath = os.path.join(FILESTORE, name)

    async with aiofiles.open(filepath, "r") as out_file:
        content = await out_file.read()

    return {"name": name, "data": content}


@app.post("/files/")
async def write_file(file: File):
    if file.filepath:
        filepath = os.path.join(FILESTORE, file.filepath)
    else:
        filepath = os.path.join(FILESTORE, file.name)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    async with aiofiles.open(filepath, "w") as out_file:
        await out_file.write(file.content)

    return {"result": "File saved successfully."}
