from datetime import date
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Log(BaseModel):
    pass


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    date: date
    content: str


class Alert(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    date: date
    content: str


class Error(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    date: date
    content: str


class OpenAIMessage(BaseModel):
    role: str
    content: str
    name: str


class Choice(BaseModel):
    index: int
    message: OpenAIMessage
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
