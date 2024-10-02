from scint.framework.components.enum import BlockEnum
from scint.framework.types.model import Model


__all__ = "Property", "Block", "Link"


class Block(Model):
    type: BlockEnum = BlockEnum.TEXT
    data: str

    @property
    def index(self):
        return self.data


class Property(Model):
    key: str
    value: Block

    @property
    def index(self):
        content = ""
        for block in self.value:
            content += block.data
            content += "\n"
        return {"role": "system", "content": content}


class Link(Model):
    id: int = None
    title: str
    anchor: int
    reference: int
    weight: float
    annotation: str
