from typing import List

from scint.framework.types.model import Model
from scint.framework.models.properties import Block


class Message(Model):
    blocks: List[Block]

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {
            "role": "assistant",
            "content": "Sent on " + self.timestamp + "\n" + content,
        }


class InputMessage(Message):
    blocks: List[Block]
    embedding: List[float] = []

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {
            "role": "user",
            "content": "Sent from Tim Kaechle on " + self.timestamp + "\n" + content,
        }


class SystemMessage(Message):
    labels: List[str] = []

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {
            "role": "system",
            "content": "Sent on " + self.timestamp + "\n" + content,
        }


class OutputMessage(Message):
    labels: List[str] = []
    annotation: str = None


class Instruction(Model):
    name: str
    blocks: List[Block] = []

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {"role": "system", "content": content}


class Prompt(Model):
    name: str
    description: str
    labels: List[str] = []
    blocks: List[Block] = []

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {"role": "system", "content": content}
