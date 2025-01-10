from __future__ import annotations

from dataclasses import field
from enum import Enum, auto
from typing import List, Dict, Any


from src.core.types import Struct
from src.models.blocks import Block


class SignalType(Enum):
    user = auto()
    assistant = auto()
    system = auto()


class Signal(Struct):
    content: List[Block] = field(default_factory=list)
    type: str = SignalType.user.name

    @property
    def model(self):
        return {"role": self.type, "content": "".join(b.data for b in self.content)}

    @property
    def string(self):
        return "".join(b.data for b in self.content)

    @classmethod
    def create(cls, content: List[Block], metadata: Dict[str, Any] = None):
        if not metadata:
            return cls(content=content, type=SignalType.user.name)

        msg_type, meta = SignalType.metadata(metadata)
        return cls(content=content, type=SignalType(msg_type), metadata=meta)

    @classmethod
    def system(cls, content: List[Block], name: str, labels: List[str], anno: str):
        return cls.create(content, {"name": name, "labels": labels, "annotation": anno})

    @classmethod
    def assistant(cls, content: List[Block], labels: List[str], anno: str):
        return cls.create(content, {"labels": labels, "annotation": anno})

    @classmethod
    def user(cls, content: List[Block]):
        return cls.create(content, {"embedding": []})
