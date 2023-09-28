from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    date: date
    content: str


class Info(BaseModel):
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
