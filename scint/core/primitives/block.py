from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from scint.core.primitives import Primitive


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Block(Model):
    type: str = "text"
    data: str

    @property
    def index(self):
        return self.data


class Link(Primitive):
    def __init__(self, title, anchor, reference, weight):
        super().__init__()
        self.id: str = Field(default_factory=lambda: str(uuid4()))
        self.title: str = title
        self.anchor: str = anchor
        self.reference: str = reference
        self.weight: float = weight
