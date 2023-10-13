from typing import Dict

from pydantic import BaseModel


class Payload(BaseModel):
    agent: str
    message: Dict[str, str]
