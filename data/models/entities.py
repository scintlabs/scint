import os
from typing import List, Optional, Sequence, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from base.observability.logging import logger
from data.models.events import Event
from data.models.functions import ModelFunction
from data.models.lifecycle import Lifecycle
from data.models.messages import Message
from data.models.prompts import Prompt, SystemPrompt


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class Organization(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    lifecycle: Lifecycle


class Team(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    organization: Organization
    lifecycle: Lifecycle


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    title: str
    email: str
    number: int
    team: str
    organization: str
    lifecycle: Lifecycle


class System(BaseModel):
    name: str = "Scint"
    lifecycle: Lifecycle = Lifecycle()


class Coordinator(Entity):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class Executor(Entity):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class Finder(Entity):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class Generator(Entity):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class Processor(Entity):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class Writer(Entity):
    id: UUID = Field(default_factory=uuid4)
    Lifecycle: Lifecycle


class CodeParser(Entity):
    pass


class TextParser(Entity):
    pass


class DataParser(Entity):
    pass


class Agent(BaseModel):
    name: str
    events: List[Event]
    messages: Union[Prompt, Message]
    functions: List[ModelFunction]
    system_prompt: SystemPrompt

    async def initialize_state(self):
        logger.info(f"Initializing {self.name}.")

    async def emitter(self, event):
        pass

    async def send_message(self, message: Message):
        logger.info(f"{self.name} sent a message.")
