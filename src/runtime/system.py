from __future__ import annotations
from typing import Any, Dict, Type

from attrs import define, field

from src.runtime.actor import Actor, Address, Envelope


@define
class ActorSystem:
    _actors: Dict[str, Actor] = field(factory=dict)
    _resources = field(default=None)
    _registry: Dict[str, Address] = field(factory=dict)

    def load(self):
        pass
        # idx = Indexes()
        # self.spawn("interpreter", Interpreter, continuity=Continuity(indexes=idx))
        # self.spawn("composer", Composer, library=Library(indexes=idx))
        # self.spawn("executor", Executor, catalog=Catalog(indexes=idx))

    def start(self, resources):
        self._resources = resources or dict()

    def shutdown(self):
        pass

    def spawn(self, name: str, actor_cls: Type[Actor], *args, **kwargs):
        if name in self._registry:
            return self._registry[name]

        instance = actor_cls(*args, **kwargs)
        instance.start()
        ref = instance.ref()
        self._registry[name] = ref
        self._actors[name] = instance
        return ref

    def tell(self, address: Address, env: Envelope):
        if not isinstance(address, Address) or not self._registry[address]:
            raise ValueError("Not a valid actor address.")
        self._registry[address].tell(env)

    def ask(self, address: Address, env: Envelope, timeout: int = None):
        if not isinstance(address, Address) or not self._registry[address]:
            raise ValueError("Not a valid actor address.")
        return self._registry[address].ask(env, timeout)

    def listen(self, timeout=None):
        pass

    def _update_resource(self, resource: Any, **kwargs):
        pass
