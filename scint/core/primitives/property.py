from typing import List
from uuid import uuid4

from pydantic import Field

from scint.core.primitives.block import Block, Model


__all__ = "Property"


class Property(Model):
    id: str = Field(default_factory=lambda: str(uuid4()))
    key: str
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
