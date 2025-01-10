from __future__ import annotations

from enum import Enum, auto
from typing import List

from src.core.types import ProcessType
from src.models.blocks import Block
from src.core.struct import Struct


class ProcessState(str, Enum):
    STARTED = auto()
    WAITING = auto()
    STOPPED = auto()


class ProcessResult(Enum):
    SUCCEEDED = auto()
    FAILED = auto()


class Process(Struct):
    def __init__(self):
        self.result: List[Block] = []

    @property
    def model(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "system", "content": content}


class Processes(metaclass=ProcessType):
    def __init__(self):
        self.processes: List[Process] = []
