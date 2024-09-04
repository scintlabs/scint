from typing import Dict

from scint.core.components import Composition
from scint.core.primitives.block import Link
from scint.services.persistence import Persistence


class Graph(Composition, Persistence):
    def __init__(self):
        super().__init__()
        self.links: Dict[str, Link] = {}
        self._compositions: Dict[str, Composition] = {}
        self.last_active_composition: Composition = None

    @property
    def compositions(self) -> Dict[str, Composition]:
        return self._compositions

    @compositions.setter
    def compositions(self, value: Dict[str, Composition]):
        self._compositions = value
        if value:
            self.last_active_composition = next(reversed(value.values()))

    def update_composition(self, key: str, composition: Composition):
        self._compositions[key] = composition
        self.last_active_composition = composition

    def __setitem__(self, key: str, value: Composition):
        self.update_composition(key, value)

    def __getitem__(self, key: str) -> Composition:
        return self._compositions[key]
