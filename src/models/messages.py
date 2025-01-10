from __future__ import annotations

from dataclasses import field
from typing import Dict, List, Optional

from src.core.types import Struct
from src.models.blocks import Block
from src.models.functions import Result


class FunctionCall(Struct):
    name: str
    arguments: Dict[str, str]
    returns: Result


class Message(Struct):
    content: List[Block] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    annotation: str = field(default_factory=str)
    embedding: List[float] = field(default_factory=list)

    @property
    def model(self):
        return {
            "role": "user",
            "content": "".join(b.data for b in self.content),
        }


class Instruction(Struct):
    content: List[Block] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    annotation: str = field(default_factory=str)
    embedding: List[float] = field(default_factory=list)

    @property
    def model(self):
        return {
            "role": "system",
            "content": "".join(b.data for b in self.content),
        }


class Prompt(Struct):
    content: List[Block] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    annotation: str = field(default_factory=str)
    embedding: List[float] = field(default_factory=list)

    @property
    def model(self):
        return {
            "role": "system",
            "content": "".join(b.data for b in self.content),
        }


class Query(Struct):
    index: Optional[str] = field(default_factory=str)
    query: Optional[str] = field(default_factory=str)
    category: Optional[str] = field(default_factory=str)
    result: List[str] = field(default_factory=list)

    @property
    def model(self):
        return {"role": "system", "content": "".join([r for r in self.result])}
