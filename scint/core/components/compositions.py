from typing import List
from scint.core.components import Composition


class Conversation(Composition):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title: str
        self.instructions = []
        self.messages = []
        self.embedding: List[float]
        self.metadata = {}
