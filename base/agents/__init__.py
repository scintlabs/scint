from typing import List

from pydantic import BaseModel

from base.processing.functions import OpenAIFunction
from base.processing import Prompt


class Agent(BaseModel):
    pass


class Assistant(Agent):
    name: str
    system_prompt: Prompt


class Coordinator(Agent):
    name: str
    system_prompt: Prompt


class Sentry(Agent):
    name: str
    system_prompt: Prompt
