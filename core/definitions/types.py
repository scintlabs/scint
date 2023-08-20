from typing import NamedTuple, List, Dict
from dataclasses import dataclass


class Fragment:
    name: str
    content: str


class Block(NamedTuple):
    content: str
    fragments: List[Fragment]


class Shard(NamedTuple):
    title: str
    blocks: List[Block]


class Function(Block):
    pass
