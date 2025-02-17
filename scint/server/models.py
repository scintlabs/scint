from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Request(Model):
    content: str
