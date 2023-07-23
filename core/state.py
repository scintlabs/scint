import os
import json


class State:
    def __init__(self, name):
        self.name = name
        self.data = load_json(f"core/assistants/{self.name}_state.json")

    def identity_constructor(self):
        self.identity_data = self.data["definitions"]["keanu"]
        self.identity = " ".join(self.identity_data["data"])
        return self.identity


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)


def save_filestore(self):
    save_json(f"core/assistants/{self.name}_state.json", self.state)
