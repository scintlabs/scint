from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, Json

from base.persistence import LifeCycle


class Tag(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    name: str
    description: str


class File(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    name: str
    format: str
    content: str


class Link(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    name: str
    description: Optional[str]
    path: HttpUrl = Field(..., description="Listof valid URLs")


class Prompt(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    prompt: str
    role: str
    lifecycle: LifeCycle


class SystemPrompt(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    system_prompt: str
    role: str = "system"
    lifecycle: LifeCycle


class FunctionalPrompt(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    system_prompt: str
    role: str
    lifecycle: LifeCycle


class FewShotPrompt(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    system_prompt: SystemPrompt
    additional_prompts: List[Prompt]
    lifecycle: LifeCycle


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str


class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    lifecycle: LifeCycle
    tasks: List[Task]


class ContentGenerator(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    objective: Task
    prompts: List[SystemPrompt]
