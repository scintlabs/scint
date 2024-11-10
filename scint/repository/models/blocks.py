from dataclasses import dataclass
from typing import List, Optional

from scint.ensemble.components.enum import Enumerator

Blocks = Enumerator(
    TEXT=type("Text", (), {}),
    CODE=type("Code", (), {}),
    IMAGE=type("Image", (), {}),
    LINK=type("Link", (), {}),
    VECTOR=type("Vector", (), {}),
)


@dataclass
class Block(Model):
    type = Blocks.TEXT
    data: str


@dataclass
class Metadata(Model):
    labels: List[str]
    annotation: str
    embedding: Optional[List[float]] = None


@dataclass
class Header(Model):
    labels: List[str]
    annotation: str
    embedding: Optional[List[float]] = None
