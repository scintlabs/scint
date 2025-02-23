from enum import Enum
from typing import Optional


class ProcessorState(Enum):
    PLANNING = ("PLANNING", None)
    PROCESSING = ("PROCESSING", None)
    VALIDATING = ("VALIDATING", None)
    CANCELLING = ("CANCELLING", None)
    RETURNING = ("COMPOSING", None)

    def __init__(self, state: str, default_next: Optional[str]):
        self.state = state
        self.default_next = default_next
        self.on_enter = lambda obj: None
        self.on_exit = lambda obj: None

    def set_hooks(self, on_enter, on_exit) -> None:
        self.on_enter = on_enter
        self.on_exit = on_exit
