from datetime import datetime, timezone
from typing import Any, Callable, Dict, NamedTuple, Optional, List

from pydantic import BaseModel, Field

from ...utils import generate_id


class Model(BaseModel):
    pass


class Block(BaseModel):
    data: str
    type: str = "text"

    def build(self):
        return self.data


class Message(Model):
    id: str = Field(default_factory=lambda: str(generate_id("msg")))
    timestamp: str = Field(default_factory=lambda: str(datetime.now(timezone.utc)))
    body: List[Block]

    def dump(self):
        content = ""
        for block in self.body:
            content += block.build()
            content += "\n"
        return {"role": "user", "content": content}


class Prompt(Model):
    body: List[Block]

    def dump(self):
        content = ""
        for block in self.body:
            content += block.build()
            content += "\n"
        return {"role": "system", "content": content}


example_message = {
    "body": [
        {
            "type": "text",
            "data": "A semantic String containing text or markdown content, including sentences, a single list item, a heading, or a paragraph.",
        },
        {"type": "code", "data": "Inline code snippets or examples."},
        {"type": "labels", "data": "semantic, keyword, labels"},
        {"type": "annotation", "data": "A sentence summarizing the interaction."},
    ],
}


instructions_prompt = Prompt(
    **{
        "body": [
            Block(
                **{
                    "type": "text",
                    "data": f"When responding, make sure all messages are sent as an array of JSON blocks following the schema below. Each response requires a valid response and classification objects. Response keys require at least one string object, while classification keys require both continuation and annotations keys. Schema as follows:",
                }
            ),
            Block(
                **{
                    "type": "text",
                    "data": str(example_message),
                }
            ),
            Block(
                **{
                    "type": "text",
                    "data": "Objects in the response String are processed sequentially, and individual Strings are separated by a line break, so each string should be a standalone component, such as a heading or paragraph. The labels block is for tagging the interaction with semantic keywords. And the annotations block enables advanced system analysis and memory encoding. Be sure both of these follow the same format as messages. Make sure ALL DATA FIELDS are STRINGS.",
                }
            ),
        ]
    }
)


class Prompts(NamedTuple):
    instructions: Optional[Prompt] = instructions_prompt


class Messages(Model):
    prompts: Prompts = Prompts()
    messages: List[Message] = []
    labels: List[List[str]] = []
    embeddings: List[List[float]] = []

    def __call__(self, *args, **kwargs):
        if not args and kwargs:
            return property(self.dump)

    def append(self, message: Message):
        self.messages.append(message)

    def build(self):
        messages = []
        for key, value in self.prompts._asdict().items():
            if value is not None:
                messages.append(value)
        messages.extend(self.messages)
        return messages

    def dump(self):
        messages = []
        for value in self.prompts:
            if value is not None:
                messages.append(value.build())
        for message in self.messages:
            messages.append(message.build())
        return messages
