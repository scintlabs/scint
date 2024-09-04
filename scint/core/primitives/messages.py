from typing import List
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import Field

from scint.core.primitives.block import Model, Block


__all__ = "InputMessage", "OutputMessage", "SystemMessage"


class Message(Model):
    id: str = Field(default_factory=lambda: str(uuid4()))
    role: str = "system"
    blocks: List[Block]
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            "%Y-%m-%d  %H:%M:%S"
        )
    )

    @property
    def index(self):
        content = ""
        for block in self.blocks:
            content += block.data
            content += "\n"
        return {
            "role": self.role,
            "content": "Sent from Tim Kaechle on "
            + datetime.now().strftime("%B %d %Y %H:%M:%S")
            + "\n"
            + content,
        }

    @property
    def sketch(self):
        content = [
            "Sent from Tim Kaechle on ",
            datetime.now().strftime("%B %d %Y %H:%M:%S"),
            "\n",
        ]
        for block in self.blocks:
            content.append(block.data)
        return "\n".join(content)


class InputMessage(Message):
    blocks: List[Block]
    embedding: List[float] = []
    role: str = "user"


class SystemMessage(Message):
    blocks: List[Block]
    annotation: str = None
    labels: List[str] = []
    commands: List[str] = []
    role: str = "system"


class OutputMessage(Message):
    role: str = "assistant"
    annotation: str = None
    labels: List[str] = []
    commands: List[str] = []
