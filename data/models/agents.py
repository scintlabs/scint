from typing import List, Optional, Sequence, Union

from pydantic import BaseModel

from base.observability.logging import logger
from data.functions.functions import ModelFunction
from data.models.events import Event
from data.models.messages import Message
from data.models.prompts import Prompt, SystemPrompt


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
