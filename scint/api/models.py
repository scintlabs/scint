from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class Response(BaseModel):
    content: str


class Request(BaseModel):
    content: str
