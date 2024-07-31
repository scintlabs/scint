from typing import List, NamedTuple, Optional

from scint.base.models import Model


class Header(Model):
    pass


class Block(Model):
    type: str
    data: str


class Prompt(Model):
    name: str
    category: str
    description: str
    labels: List[str]
    body: List[Block]


class PromptFields(NamedTuple):
    persona: Optional["Prompt"] = None
    modifier: Optional["Prompt"] = None
    instructions: Optional["Prompt"] = None
    constraints: Optional["Prompt"] = None


class Message(Model):
    sender: str
    receiver: str
    timestamp: str = None
    annotation: str = None
    labels: List[str] = None
    embedding: List[float] = None
    body: List[Block]
