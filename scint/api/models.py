from __future__ import annotations

from typing import Dict

from pydantic import BaseModel


class Response(BaseModel):
    pass


class Request(BaseModel):
    message: Dict[str, str]
