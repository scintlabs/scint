from __future__ import annotations

from attrs import define


from src.core.agents.dispatcher import Dispatcher


@define
class ActorSystem:
    _dispatcher: Dispatcher = Dispatcher()
