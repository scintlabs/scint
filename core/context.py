import os
import json
from core.environment import Environment
from core.providers.openai import gpt
from core.state import State


class Context:
    def __init__(self):
        self.context = Environment.load_json("core/state/context.json")
        self.dialogue = []

    def prune(self, e):
        self.event = self.events[e]

    @staticmethod
    def save(self):
        Environment.save_json(f"core/state/context.json", self.context)


class ContextObserver:
    def __init__(self):
        self.context = Context()
