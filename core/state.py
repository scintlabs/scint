import os

from util.env import envar
from util.logging import logger

APPNAME = "scint"
APPDATA = os.path.join(envar("XDG_DATA_HOME"), APPNAME)


class State:
    PROCESSING = "processing"
    GENERATING = "generating"
    CHATTING = "chatting"
    SEARCHING = "searching"
    IDLE = "idle"

    def __init__(self):
        # Initial state is idle
        self.current_state = self.IDLE

    def set_state(self, new_state):
        if new_state in [
            self.PROCESSING,
            self.GENERATING,
            self.CHATTING,
            self.SEARCHING,
            self.IDLE,
        ]:
            self.current_state = new_state
        else:
            raise ValueError(f"Invalid state: {new_state}")

    def get_state(self):
        return self.current_state

    def is_idle(self):
        return self.current_state == self.IDLE

    def __str__(self):
        return f"AI Assistant is currently: {self.current_state}"

    def __init__(self):
        """Object for managing application state."""
