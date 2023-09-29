import os
from typing import Optional

from base import System


def envar(var: str) -> Optional[str]:
    return os.environ.get(var)


SYSTEM = System()
DATA_STORE = os.path.join(envar("XDG_DATA_HOME") or ".local/share", SYSTEM.name)
