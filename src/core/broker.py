from __future__ import annotations

from typing import Any, Dict

from attrs import define, field

from src.core.schema.context import Context
from src.core.schema.outline import Outline
from src.core.schema.records import Metadata, Message
from src.runtime.actor import Actor, ActorRef


@define(slots=True)
class Envelope:
    sender: str = field(default=None)
    payload: Any = field(default=None)
    correlation: str = field(default=None)
    metadata: Metadata = field(default=None)

    @classmethod
    def create(cls, sender: str, payload: Any):
        return cls(sender=sender, payload=payload, metadata=Metadata())


@define
class Broker(Actor):
    _registry: Dict[str, ActorRef] = field(factory=dict)

    async def on_receive(self, env: Envelope):
        mdl = env.payload
        if isinstance(mdl, Message):
            target = self._registry.get("interpreter")
        elif isinstance(mdl, Context):
            target = self._registry.get("composer")
        elif isinstance(mdl, Outline):
            target = self._registry.get("executor")
        else:
            target = None

        if target is None:
            raise RuntimeError("Dispatcher missing target for " f"{type(mdl).__name__}")
        target.tell(mdl, sender=self.ref())
