from typing_extensions import List
from pydantic import BaseModel

from scint.base.models import Model
from scint.base.models.messages import Message, PromptFields


class Attributes(BaseModel):
    pass


class Prompts(Attributes):
    fields: PromptFields = PromptFields()
    additional: List["Prompt"] = []

    def dump(self):
        prompts = []
        for field in self.fields:
            if field is not None:
                prompts.append(field.dump())
        if self.additional:
            prompts.extend(prompt.dump() for prompt in self.additional)
        return prompts

    def __call__(self, *args, **kwargs):
        if not args and kwargs:
            return self.items

    @property
    def items(self):
        return {**self.fields._asdict(), "additional": self.additional}


class Messages(Model):
    items: List[Message] = []
    labels: List[List[str]] = []
    embeddings: List[List[float]] = []

    def add(self, message: Message):
        self.items.append(message)

    def dump(self):
        return [item.dump() for item in self.items]

    def __call__(self, *args, **kwargs):
        if not args and kwargs:
            return self.items
