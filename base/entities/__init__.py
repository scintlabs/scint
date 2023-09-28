from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.persistence import LifeCycle


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    lifecycle: LifeCycle


class System(Entity):
    id: UUID = Field(default_factory=uuid4)
    name: str = "Scint"
    lifecycle: LifeCycle = LifeCycle()


class Finder(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Processor(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Generator(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
