from enum import Enum
from typing import Dict
from uuid import UUID, uuid4

from data.models.entities import User
from data.models.lifecycle import Lifecycle

USER = User(
    name="Tim Kaechle",
    title="Founda",
    email="timothy.kaechle@me.com",
    number=8675309,
    team="Scint Balls",
    organization="Scint",
    lifecycle=Lifecycle(),
)


logit_bias: Dict = {1102: -100, 4717: -100, 7664: -100}
