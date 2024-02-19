import uuid
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel, Field


class Tag(BaseModel):
    name: str
    description: str


class Taggable(BaseModel):
    tags: List[Tag] = []


class Timestamp(BaseModel):
    date: datetime = Field(default_factory=lambda: datetime.now().date())
    time: datetime = Field(default_factory=lambda: datetime.now().time())

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d')} {self.time.strftime('%H:%M')}]"


class Identifiable(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class User(Identifiable, BaseModel):
    name: str
    email: str
    accounts: List[Tag]


class Project(Identifiable, Taggable, BaseModel):
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    additional_info: Optional[Dict[str, str]] = None
    github_repo: str


class SystemInfo(Identifiable, BaseModel):
    os_name: str
    os_version: str
    architecture: str
    python_version: str
    additional_info: Dict[str, str]


class NodeIndex(Identifiable, Taggable, BaseModel):
    name: str
    summary: str


class Node(Identifiable, Taggable, BaseModel):
    data: str
    size: int
    first_sibling: "Node"
    second_sibling: Optional["Node"] = None
    embedding: List[int] = Field(default_factory=list)


class Message(Identifiable, BaseModel):
    role: str
    content: str
    sender: str
    receiver: str


class SystemPrompt(Message):
    role: str = "system"


class SystemMessage(Message):
    role: str = "system"
    sender: str = "System"
    receiver: str = "System"


class UserMessage(Message):
    role: str = "user"
    sender: str = "User"
    receiver: str = "Chat"


class AssistantMessage(Message):
    role: str = "assistant"


class SearchMessage(Message):
    role: str = "system"


class DataMessage(Message):
    role: str = "system"
    processed: bool = False
    node: Optional[Node]
