from typing import List

from scint.framework.types.model import Model
from scint.framework.models.properties import Block


class File(Model):
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

    @property
    def sketch(self):
        content = [
            "Sent on ",
            self.timestamp,
            "\n",
        ]
        for block in self.blocks:
            content.append(block.data)
        return "\n".join(content)
