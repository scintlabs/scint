from typing import List, Optional
from pydantic import BaseModel, Json


class OpenAIMessage(BaseModel):
    role: str
    content: str
    name: str | None

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "name": self.name,
        }


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
