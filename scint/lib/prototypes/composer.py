from __future__ import annotations

from scint.lib.prototypes.scheduler import Observe
from scint.lib.schemas.context import ContextProvider
from scint.lib.types.struct import Struct
from scint.lib.types.traits import Trait


class Compose(Trait):
    def compose(self):
        pass


class Composer(Struct):
    context = ContextProvider()
    traits = (Compose, Observe)
