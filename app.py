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


# @app.post("/files/")
# async def write_file(name: str, content: File, filepath: Optional[str]):
#     if filepath:
#         f = filepath + name
#     else:
#         f = name
#     with open(f, "w", encoding="utf-8", errors="ignore") as file:
#         f.write(content)  # type: ignore
#     return {"message": "File written."}


# @app.post("/write/{file_path:path}")
# async def write_file(file: File):
#     with open(file.filename, "w", encoding="utf-8") as f:
#         f.write(file.content)
#     return {"message": "File written successfully."}


# @app.post("/files/")
# def create_file(file_name: UploadFile = File(...)):
#     file_path = file_directory / Path(file_name)
#     with open(file_path, "wb") as buffer:
#         buffer.write(file.file.read())
#     return {"message": "File uploaded successfully.", "file_name": file.filename}


# @app.get("/files/{file_name}")
# def read_file(file_name: str):
#     file_path = file_directory / Path(file_name)
#     if file_path.exists():
#         return FileResponse(file_path)
#     else:
#         return {"error": "File not found."}


# @app.post("/files/{file_name}")
# async def create_or_update_file(filename: str, file: UploadFile = File(...)):
#     file_path = file_directory / Path(file_name)
#     with file_path.open("wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"filename": filename}
