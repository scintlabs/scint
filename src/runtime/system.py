from __future__ import annotations

from typing import TypeAlias, Union

from attrs import define


from src.core.agents.dispatcher import Dispatcher
from src.model import Context, Outline, Process, Content


Model: TypeAlias = Union[Context, Outline, Process, Content]


@define
class ActorSystem:
    _dispatcher: Dispatcher = Dispatcher()
