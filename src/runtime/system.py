from __future__ import annotations
from typing import Dict, Type

from attrs import define, field

from src.base.actor import Actor, Address
from src.continuity.threads import Threads
from src.runtime.agents import Interpreter, Composer, Executor
from src.runtime.broker import Broker, Envelope
from src.services.indexes import Indexes
from src.services.storage import Storage

resources = {"indexes": Indexes(), "storage": Storage(), "threads": Threads()}


@define
class System(Actor):
    _broker: Broker = Broker()
    _actors: Dict[str, Actor] = field(factory=dict)

    def start(self, *args, **kwargs):
        self.spawn("broker", Broker, **resources)
        self.spawn("interpreter", Interpreter)
        self.spawn("composer", Composer)
        self.spawn("executor", Executor)

    def stop(self):
        pass

    def spawn(self, name: str, actor: Type[Actor], *args, **kwargs):
        if name in self._actors:
            return self._actors[name]

        self._actors[name] = actor(*args, **kwargs)
        address = self._actors[name].address()
        self._actors[name] = address
        return address

    def tell(self, address: Address, env: Envelope):
        if not isinstance(address, Address) or not self._registry[address]:
            raise ValueError("Not a valid actor address.")
        self._directory[address].tell(env)

    def ask(self, address: Address, env: Envelope, timeout: int = None):
        if not isinstance(address, Address) or not self._registry[address]:
            raise ValueError("Not a valid actor address.")
        return self._directory[address].ask(env, timeout)

    def listen(self, timeout=None):
        pass
