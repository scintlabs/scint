from enum import Enum


class State(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DISABLED = "disabled"
