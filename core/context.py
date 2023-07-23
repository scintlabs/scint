import os
import json
from core.environment import load_files, load_json
from core.providers.openai import gpt
from core.state import State
from core.capabilities.functions import functions


class Context:
    def __init__(self, name):
        self.name = name
        self.context = load_json(f"core/assistants/{self.name}_context.json")
        self.functions = functions

    def functions(self):
        return self.functions

    def dialogue(self):
        self.messages = []

    def events(self):
        self.events = self.state.events

        def prune(self, e):
            self.event = self.events[e]

    def save_filestore(self):
        save_json(f"core/assistants/{self.name}_state.json", self.state)
