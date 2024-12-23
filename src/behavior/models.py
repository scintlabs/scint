from typing import Optional

from ..base import Model
from ..util.helpers import generate_timestamp


class Block(Model):
    data: str


class Event(Model):
    timestamp: str = generate_timestamp()
    name: str
    data: str
    result: Optional[str] = None

    @property
    def schema(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "system", "content": content}


__all__ = Event
