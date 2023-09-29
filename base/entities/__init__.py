from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.persistence.lifecycle import LifeCycle


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Coordinator(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Executor(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Finder(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Generator(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Processor(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle


class Writer(Entity):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
