from __future__ import annotations

from functools import singledispatchmethod
from typing import Dict

from attrs import define, field

from src.base.actor import Actor
from src.compose.composer import Composer
from src.execute.executor import Executor
from src.interpret.interpreter import Interpreter


@define
class Broker:
    _directory: Dict[str, Actor] = field(factory=dict)

    async def ask(self, actor, msg):
        if actor in self._directory.keys():
            return await self._directory[actor].ask(msg)

    @singledispatchmethod
    def put(self, actor, msg):
        raise TypeError(f"{actor} not found.")

    @put.register(Interpreter)
    def _(self, actor, msg):
        self._interpret.tell(msg)

    @put.register(Executor)
    def _(self, actor, msg):
        self._interpret.tell(msg)

    @put.register(Composer)
    def _(self, actor, msg):
        self._interpret.tell(msg)

    def register(self, actor: Actor):
        if isinstance(actor, Actor):
            self._directory[type(actor).__name__] = actor
