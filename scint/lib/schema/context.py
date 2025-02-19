from __future__ import annotations

from asyncio.queues import PriorityQueue
from collections import deque
from typing import Deque, List

from scint.lib.schema.models import Model, Prompt
from scint.lib.schema.signals import Event, Message, Response
from scint.lib.types.factory import Factory
from scint.lib.types import Struct
from scint.lib.types.tasks import Task
from scint.lib.types.tools import Tool, ToolKit, Tools


class TemporalState(Struct):
    events: List[Event] = PriorityQueue()
    current: ActiveState
    prev: ActiveState
    next: ActiveState


class SemanticState(Model):
    intention: Task = None
    prompts: List[Prompt] = []
    messages: List[Message | Response] = []
    tasks: List[Task] = []
    tools: List[Tool] = []


class ActiveState(Model):
    goal: Task = None
    events: List[Event] = []
    tasks: List[Task] = []
    messages: List[Message | Response] = []
    tools: List[Tool] = []


class Context(Struct):
    active: ActiveState
    semantic: SemanticState
    temporal: TemporalState


class ContextKit(ToolKit):
    _active: ActiveState
    _semantic: SemanticState

    def active_state(self):
        messages = [self._active.goal, *self._active.events, *self._active.messages]
        return {"messages": messages, "tools": self._active.tools}

    def semantic_state(self):
        messages = [self._active.goal, *self._active.events, *self._active.messages]
        return {"messages": messages, "tools": self._active.tools}


class ContextFactory(Factory):
    ActiveState = ("Active", (ActiveState,), {})
    SemanticState = ("SemanticState", (SemanticState,), {})
    TemporalState = ("TemporalState", (TemporalState,), {})
