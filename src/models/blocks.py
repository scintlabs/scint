from __future__ import annotations

from enum import Enum, auto
from typing import Optional

from src.core.types import Struct


class BlockType(Enum):
    TEXT = auto()
    CODE = auto()
    FILE = auto()
    IMAGE = auto()


class Block(Struct):
    data: str
    type: BlockType


class TextBlock(Struct): ...


class CodeBlock(Struct):
    language: str
    version: Optional[str] = None


class ImageBlock(Struct):
    dimensions: Optional[tuple[int, int]] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    format: Optional[str] = None


class FileBlock(Struct):
    file_name: Optional[str] = None
    file_path: Optional[Block] = None
    head: Optional[Block] = None
    tail: Optional[Block] = None
    prev_block: Optional[Block] = None
    next_block: Optional[Block] = None
