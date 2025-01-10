from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional

from src.core.struct import Struct
from src.models.blocks import Block


class TaskState(str, Enum):
    STARTED = auto()
    WAITING = auto()
    STOPPED = auto()


class TaskResult(Enum):
    SUCCEEDED = auto()
    FAILED = auto()


class Task(Struct):
    name: Optional[str] = None
    content: List[Block] = []
    result: List[str] = []

    @property
    def model(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "system", "content": content}
