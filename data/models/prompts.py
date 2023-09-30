from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Prompt(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    role: str


class SystemPrompt(Prompt):
    role: str = "system"
    content: str


class AssistantPrompt(Prompt):
    role: str = "assistant"


class UserPrompt(Prompt):
    role: str = "user"


class FewShotPrompt(Prompt):
    content: SystemPrompt
    prompts: List[Prompt]


class FunctionalPrompt(Prompt):
    role: str = "system"
    content: str
