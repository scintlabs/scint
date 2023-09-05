import os
from typing import Dict

from base.definitions.types import Entity, Role
from util.env import envar

SYSTEM = Entity(name="scint", role="system")
DATA = os.path.join(envar("XDG_DATA_HOME"), SYSTEM.name)
logit_bias: Dict = {1102: -100, 4717: -100, 7664: -100}

ASSISTANT = Entity(name="Assistant", role="assistant")
USER = Entity(name="Tim", role=Role.user)
