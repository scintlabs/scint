from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, Json

from base.persistence.lifecycle import LifeCycle
from base.processing.prompts import SystemPrompt

from typing import List


class Tag(BaseModel):
    tag: str
    description: str


class File(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    format: str
    content: str


class Link(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    name: str
    description: Optional[str]
    path: HttpUrl = Field(..., description="Listof valid URLs")


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
