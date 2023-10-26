from __future__ import annotations
from typing import Dict

from pydantic import BaseModel, ValidationError


class Request(BaseModel):
    worker: str
    message: Dict[str, str]


class Response(BaseModel):
    pass


class Message(BaseModel):
    pass


class File(BaseModel):
    pass
