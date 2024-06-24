from datetime import time
import traceback
from typing import Self
from uuid import uuid4
from enum import Enum, auto
from abc import ABC, abstractmethod

import numpy as np

from scint.core import library
from scint.core.composer import Composer
from scint.core.data.region import Region
from scint.core.data.graph.location import Location
from scint.core.data.containers.collections import Messages, Prompts, Functions
from scint.messaging.models import Message, UserMessage, SystemMessage, Arguments
from scint.intelligence.provider import intelligence
from scint.intelligence.models import Request
from scint.support.types import List, Dict, Tuple, Any
from scint.support.logging import log


from abc import ABC, abstractmethod
from enum import Enum, auto
from uuid import uuid4


class ContextObserver:
    def update(self, context, new_state):
        raise NotImplementedError("Observer update method not implemented.")


class State(Enum):
    transitory = auto()
    busy = auto()
    active = auto()
    inactive = auto()


class AbstractContext(ABC):
    def __init__(self):
        self.id = str(uuid4())
        self._state = State.inactive
        self._observers = []

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
        self._notify_observers()

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def _notify_observers(self):
        for observer in self._observers:
            observer.update(self)

    @abstractmethod
    async def process(self, message):
        pass

    @abstractmethod
    async def at(self, location, message):
        pass

    async def _function_call(self, arguments: Arguments):
        log.info(f"Calling function with context {self.id}.")
        func_to_call = library.read("functions")
        async for new_res in func_to_call(**arguments.arguments):
            self.messages.append(new_res)
            yield await self._completion()

    @property
    def _metadata(self):
        return {
            "id": self.id,
            "prompts": self.prompts,
            "messages": self.messages,
            "functions": self.functions,
        }


class Context(AbstractContext):
    def __init__(self):
        self.intelligence = intelligence
        self.id = str(uuid4())
        self._state = State
        self._observers = []
        self.composer = None
        self.prompts = None
        self.messages = None
        self.functions = None
        self.procedure = None
        self.location = None
        self.containers = None
        self.metadata = self._metadata

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state != value:
            self._state = value
            self._notify_state_change(value)

    def _notify_state_change(self, new_state):
        for observer in self._observers:
            observer.update(self, new_state)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    async def prepare(self, location, message):
        log.info(f"Preparing context {self.id}.")
        self.state.transitory
        if message:
            await self._compose(message)
        await self._enter(location)
        if self.location:
            self.state.active
        return await self.process(message)

    async def process(self, message: Message):
        log.info(f"Processing message with context {self.id}.")
        self.state.busy
        self.messages.append(message)
        async for response in self._completion():
            self.state.active
            yield response

    async def _enter(self, location: Location):
        log.info(f"Entering  {self.id}.")
        location.anchor(self)
        self.containers = location.containers
        return

    async def _compose(self, message):
        log.info(f"Composing context {self.id}.")
        await self.composer.generate_params()
        prompts, funcs = await self.composer.compose(self.metadata)
        if prompts:
            self.prompts.extend(prompts)
        if funcs:
            self.functions.refresh(funcs)
            self.function_choice = "auto"

    async def _completion(self):
        log.info(f"Generating completion with context {self.id}.")
        try:
            async for response in self.intelligence.process(Request(**self.metadata)):
                self.messages.append(response)
                if isinstance(response, Arguments):
                    async for func_res in self._function_call(response):
                        self.state.active
                        yield func_res
                elif isinstance(response, Message):
                    self.state.active
                    yield response
        except Exception as e:
            log.error(f"Exception: {e}\n{traceback.format_exc()}")

    async def _function_call(self, arguments: Arguments):
        log.info(f"Calling function with context {self.id}.")
        func_to_call = library.read("functions")
        async for new_res in func_to_call(**arguments.arguments):
            self.messages.append(new_res)
            yield self.completion()

    def _exit(self, location):
        log.info(f"Removing context from location {location.id}.")
        self.messages = None
        del self.messages
        location.anchor(location)

    @property
    def _metadata(self):
        return {
            "id": self.id,
            "prompts": self.prompts,
            "messages": self.location,
            "functions": self.functions,
        }
