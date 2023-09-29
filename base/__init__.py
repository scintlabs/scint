from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.persistence.lifecycle import LifeCycle


class Organization(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    lifecycle: LifeCycle


class Team(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    organization: Organization
    lifecycle: LifeCycle


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    title: str
    email: str
    number: int
    team: str
    organization: str
    lifecycle: LifeCycle


class System(BaseModel):
    name: str = "Scint"
    lifecycle: LifeCycle = LifeCycle()
