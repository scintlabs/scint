from typing import Any, List
from scint.base.models import Model


class Block(Model):
    data: List[Any]


class Annotations(Block):
    data: List[str]


class Embedding(Block):
    data: List[float]


class Link(Block):
    data: List[float]


class Speech(Block):
    data: List[float]


class File(Block):
    data: List[float]
