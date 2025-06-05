from __future__ import annotations

from typing import Dict, Type

from attrs import field

from src.services.indexes import Indexes

from .composer import Composer
from .executor import Executor
from .interpreter import Interpreter
from src.core.resources.catalog import Catalog
from src.core.resources.continuity import Continuity
from src.core.resources.library import Library
from src.model import Context, Outline, Message
from src.runtime.actor import Actor, ActorRef
from src.model.records import Envelope
from src.runtime.protocol import agentic


@agentic
class Dispatcher(Actor):
    _registry: Dict[str, ActorRef] = field(factory=dict)
    _actors: Dict[str, Actor] = field(factory=dict)

    def load(self):
        idx = Indexes()
        self.spawn("interpreter", Interpreter, continuity=Continuity(indexes=idx))
        self.spawn("composer", Composer, library=Library(indexes=idx))
        self.spawn("executor", Executor, catalog=Catalog(indexes=idx))

    def spawn(self, name: str, actor_cls: Type[Actor], *args, **kwargs):
        if name in self._registry:
            return self._registry[name]

        instance = actor_cls(*args, **kwargs)
        instance.start()
        ref = instance.ref()
        self._registry[name] = ref
        self._actors[name] = instance
        return ref

    async def on_receive(self, env: Envelope):
        mdl = env.model
        print(env)
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


# @agentic
# class Dispatcher(Actor):
#     _registry: Dict[str, ActorRef] = field(factory=dict)

#     def load(self):
#         idx = Indexes()
#         self.spawn("executor", Executor, Catalog(indexes=idx))
#         self.spawn("composer", Composer, Library(indexes=idx))
#         self.spawn("interpreter", Interpreter, Continuity(indexes=idx))

#     def spawn(self, name: str, actor: Actor, *args):
#         if name in self._registry:
#             return self.ref(name)

#         instance = actor(args)
#         instance.start()
#         ref = instance.ref()
#         self._registry[name] = ref
#         return ref

#     def ref(self, name: str):
#         return self._registry[name]

#     async def on_receive(self, env: Envelope):
#         model = env.model
#         if isinstance(model, Message):
#             int = self._registry["interpreter"]
#             int.tell(env)
#         elif isinstance(model, Context):
#             cmp = self._registry["composer"]
#             cmp.tell(env)
#         elif isinstance(model, Outline):
#             exe = self._registry["executor"]
#             exe.tell(env)
