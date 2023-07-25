import os
import json
from core.environment import Environment
from core.providers.openai import gpt
from core.state import State


class Context:
    def __init__(self):
        self.env = Environment()
        self.data, self.messages, self.methods, self.context = Environment.load_state()

    def editor(self):
        self.buffer = env.buffers.editor_buffer

    def dialogue(self):
        self.dialogue = []
        self.dialogue_compressed = []

    def prune(self, e):
        self.event = self.events[e]

    def methods(self):
        compression = self.methods["compression"]
        organizing = self.methods["organizing"]
        validation = self.methods["validation"]
        refactoring = self.methods["refactoring"]
        recursive = self.methods["recursive"]
        lateral = self.methods["lateral"]
        return print(
            compression, organizing, validation, refactoring, recursive, lateral
        )


def context(func):
    def wrapper():
        func()

    return wrapper
