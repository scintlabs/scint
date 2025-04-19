from __future__ import annotations

from typing import Dict

from attrs import define, field

from src.core.broadcast import Broadcast
from src.core.types.context import Session
from src.core.types.ensemble import Ensemble, Index


@define
class Continuity:
    broadcast: Broadcast = Broadcast()
    ensembles: Dict[str, Ensemble] = field(factory=dict)
    indexes: Dict[str, Index] = field(factory=dict)
    sessions: Dict[str, Session] = field(factory=dict)

    def register(self, ensemble: Ensemble):
        self.ensembles[ensemble.name] = ensemble
        for k, v in self.ensembles.items():
            for index_name, index in v.indexes.items():
                self.indexes[k] = index

            self.broadcast.subscribe(k, v.handle)
            print(f"Subscribing {k}")
