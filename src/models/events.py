from __future__ import annotations

from dataclasses import field
from enum import Enum
from typing import List

from src.core.types import Struct
from src.models.blocks import Block


class EventType(Enum):
    pass


class Event(Struct):
    content: List[Block] = field(default_factory=list)

    @classmethod
    def create(cls, content: List[Block]): ...

    @property
    def model(self):
        return {"role": self.type, "content": "".join(b.data for b in self.content)}
