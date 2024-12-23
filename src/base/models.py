from typing import Any, Optional, List, Union

from pydantic import BaseModel, ConfigDict

from src.util.helpers import generate_timestamp


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def schema(self):
        return self.model_dump()


class Block(Model):
    data: str


class Event(Model):
    timestamp: str = generate_timestamp()
    name: str
    data: str
    result: Optional[str] = None

    @property
    def schema(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "system", "content": content}


class Prompt(Model):
    name: str
    description: str
    content: List[Block] = []
    labels: List[str] = []
    embedding: List[float] = []

    @property
    def schema(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "system", "content": content}


class InputMessage(Model):
    content: List[Block] = []
    embedding: List[float] = []

    @property
    def schema(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "user", "content": content}


class OutputMessage(Model):
    content: List[Block]
    labels: List[str]
    annotation: str

    @property
    def schema(self):
        content = ""
        for b in self.content:
            content += b.data
        return {"role": "assistant", "content": content}


class Memory(Model):
    base: List[Prompt] = []
    data: List[Any] = []
    messages: List[Union[InputMessage, OutputMessage]] = []
    knowledge: List[Any] = []

    def update(self, model: Model):
        self.messages.append(model)

    @property
    def schema(self):
        return {"messages": [m.schema for m in self.messages]}
