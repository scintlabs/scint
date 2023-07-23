import os
import json
from core.environment import Environment


class State:
    def __init__(self):
        self.data = Environment.load_json(f"core/state/data.json")
        self.messages = Environment.load_json(f"core/state/messages.json")
        self.methods = Environment.load_json(f"core/state/methods.json")

    def core(self):
        self.identity_data = self.data["definitions"]["keanu"]
        self.identity = " ".join(self.identity_data["data"])
        return self.identity

    @staticmethod
    def save(self):
        Environment.save_json(f"core/state/data.json", self.data)
        Environment.save_json(f"core/state/messages.json", self.messages)
        Environment.save_json(f"core/state/methods.json", self.methods)


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def save(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)


def save_filestore(self):
    save_json(f"core/assistants/{self.name}_state.json", self.state)
