from typing import NamedTuple, List, Dict
from dataclasses import dataclass


class Fragment:
    content: str
    properties: object = {"content": {"model": "statement", "type": "string"}}


class Block(NamedTuple):
    content: str
    fragments: List[Fragment]


class Shard(NamedTuple):
    title: str
    paragraphs: List[Block]


class Function(Block):
    pass


class Parameters(NamedTuple):
    content: Dict[str, str]


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Choice:
    index: int
    message: Message
    finish_reason: str


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ApiResponse:
    id: str
    object: str
    created: int
    choices: List[Choice]
    usage: Usage
