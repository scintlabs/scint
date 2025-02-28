from __future__ import annotations

import json
from typing import Any, List, Optional, Type

from redis.client import Redis

from src.types.service import Provider
from src.types.base import Index, Model
from src.types.signals import Message, SystemMessage, UserMessage
from src.schemas.tasks import Task

_indices = None
_recall = None
_state = Provider(
    name="Redis",
    client=Redis,
    settings={"host": "localhost", "port": 6379, "db": 0},
)


class IndexState(Model):
    history: Optional[Index] = None
    knowledge: Optional[Index] = None

    def _update(self, *args):
        pass


class RecallState(Model):
    data: List[Model] = []

    def _update(self, *args):
        pass


class ActiveState(Model):
    system: List[SystemMessage] = []
    data: List[Model] = []
    tasks: List[Task] = []
    messages: List[UserMessage | Message] = []

    def update(self, *args):
        for a in args:
            if isinstance(a, Task):
                self.tasks.append(a)
            if isinstance(a, UserMessage):
                self.messages.append(a)


class StateResource(Model):
    owner: str
    index_state: IndexState = IndexState()
    recall_state: RecallState = RecallState()
    active_state: ActiveState = ActiveState()

    def update(self, *args):
        self.active_state.update(*args)
        c = Continuity()
        c._update_resource(self.owner, self.model_dump_json())

    @property
    def model(self):
        messages = []
        for m in self.active_state.system:
            messages.append(m.model)
        for m in self.active_state.messages:
            messages.append(m.model)
        return {"messages": messages}


class State:
    def __set_name__(self, owner, name):
        self.service = Continuity()
        self.name = name

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
        if instance is not None:
            self.key = instance.type
            self.instance = instance
            data = self.service.get_resource(self.key)
            self._update_resource(self.key, data)
            instance._state = StateResource(owner=self.key).model_validate_json(data)
            return instance._state
        return self

    def __set__(self, instance, value):
        raise AttributeError("Cannot set immutable state directly.")

    def _update_resource(self, key, data):
        self.service._update_resource(key, data)


class Continuity:
    def __init__(self):
        self.state = _state.client()

    def get_resource(self, key: str):
        res = self.state.get(key)
        if res is None:
            state = StateResource(owner=key)
            data = state.model_dump()
            string = json.dumps(data)
            self._update_resource(key, string)
            return data
        return res

    def _update_resource(self, key: str, data: str):
        self.state.set(key, data)
