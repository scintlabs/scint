import os
import json


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)


class State:
    def __init__(self, name):
        self.name = name
        self.store = load_json(f"core/assistants/{self.name}/store.json")
        self.self = load_json(f"core/assistants/{self.name}/self.json")
        self.events = load_json(f"core/assistants/{self.name}/events.json")
        self.tasks = load_json(f"core/assistants/{self.name}/tasks.json")
        self.data = load_json(f"core/assistants/{self.name}/data.json")

    def save_filestore(self):
        save_json(f"core/assistants/{self.name}/store.json", self.store)
        save_json(f"core/assistants/{self.name}/self.json", self.self)
        save_json(f"core/assistants/{self.name}/events.json", self.events)
        save_json(f"core/assistants/{self.name}/tasks.json", self.tasks)
        save_json(f"core/assistants/{self.name}/data.json", self.data)
