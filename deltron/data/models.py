import uuid
from typing import Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel, AnyHttpUrl, DirectoryPath, FilePath, Union, Field


class Timestamp(BaseModel):
    date: datetime
    time: datetime
    timezone: str

    @classmethod
    def now(cls):
        current_time = datetime.now()
        return cls(date=current_time, time=current_time, timezone=current_time.strftime("%z"))

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d')} {self.time.strftime('%H:%M')} {self.timezone}]"


class Identifiable(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created: Timestamp = Field(default_factory=Timestamp.now)
    updated: Optional[Timestamp] = None

    class Config:
        arbitrary_types_allowed = True


class Tag(BaseModel):
    name: str
    description: str


class Taggable(BaseModel):
    tags: List[Tag] = []


class Link(BaseModel):
    target: Union[AnyHttpUrl, FilePath, DirectoryPath]
    description: str

    def __str__(self):
        return f"Link(target={self.target}, description={self.description})"


class RootNode(Identifiable, Taggable, BaseModel):
    name: str
    type: str
    summary: str
    first_child: "Node"
    second_child: "Node"


class Node(Identifiable, Taggable, BaseModel):
    size: int
    first_sibling: "Node"
    second_subling: Optional["Node"]
    embedding: List[int] = Field(default_factory=list)


class Message(BaseModel):
    role: str
    content: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created: datetime = Field(default_factory=datetime.now)

    def data_dump(self):
        return {
            "role": self.role,
            "content": self.content,
        }


class SystemPrompt(Identifiable, Message):
    role: str = "system"


class SystemMessage(Identifiable, Message):
    role: str = "system"


class UserMessage(Identifiable, Message):
    role: str = "user"


class AssistantMessage(Identifiable, Message):
    role: str = "assistant"


class SearchMessage(Identifiable, Message):
    role: str = "system"


class DataMessage(Identifiable, Message):
    role: str = "system"
    processed: bool = False
    node: Optional[Node]


class MessageThread(Identifiable, Taggable, BaseModel):
    messages: List[UserMessage | AssistantMessage]


class ProcessThread(Identifiable, Taggable, BaseModel):
    messages: List[DataMessage | SystemMessage]


class SearchThread(Identifiable, Taggable, BaseModel):
    messages: List[SearchMessage | SystemMessage]


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


class Context(Identifiable, BaseModel):
    user: User
    system_prompt: SystemPrompt
    thread: MessageThread | ProcessThread | SearchThread
    project: Optional[Project]
    system: Optional[SystemInfo]
    files: List[RootNode]
