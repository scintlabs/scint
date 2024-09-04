from typing import List
from uuid import uuid4

from pydantic import Field


from scint.core.primitives.block import Block, Model
from scint.core.primitives.messages import InputMessage


__all__ = "Loop", "Condition", "Transition"


class Instruction(Model):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    blocks: List[Block] = []

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {"role": self.role, "content": content}

    @property
    def sketch(self):
        content = []
        for block in self.blocks:
            content.append(block.data)
        return "\n".join(content)


class Prompt(Instruction):
    description: str
    labels: List[str] = []
    role: str = "system"


class Loop(Instruction):
    iterations: int = 1


class Condition:
    def __init__(self, assertion):
        self.assertion = assertion

    async def check(self, message):
        return self.assertion


class Transition:
    def __init__(self, condition: Condition, target: str):
        self.condition = condition
        self.target = target

    async def can_transition(self, message: InputMessage):
        return await self.condition.check(message)
