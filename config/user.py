from enum import Enum
from typing import Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base import User
from base.persistence.lifecycle import LifeCycle

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
