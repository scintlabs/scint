from typing import Dict

from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.persistence import LifeCycle
from base import User

USER = User(
    name="Tim Kaechle",
    title="Founda",
    email="timothy.kaechle@me.com",
    number=8675309,
    team="Scint Balls",
    organization="Scint",
    lifecycle=LifeCycle(),
)

logit_bias: Dict = {1102: -100, 4717: -100, 7664: -100}


class Role(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    role: Role
    lifecycle: LifeCycle
