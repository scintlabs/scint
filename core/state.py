import os
import json
from core.environment import Environment


class State:
    def __init__(self):
        self.data, self.messages, self.methods, self.context = Environment.load_state()

    def core(self):
        self.system_message = self.data["core"]["scint"][0]
        return self.system_message
