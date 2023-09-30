from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from data.models.artifacts import Link
from data.models.lifecycle import Lifecycle
from data.prompts.prompts import SystemPrompt


class File(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    format: str
    content: str
    path: Link


class Directory(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str


class Link(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    target: Union[File, Directory]
    directory: Optional[Directory]


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str


class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    lifecycle: Lifecycle
    tasks: List[Task]


class ContentGenerator(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    objective: Task
    prompts: List[SystemPrompt]
