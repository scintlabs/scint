import json
from . import process
from .processes.context import summarize

# TODO: Connect to db

class Context:
    def __init__(self):
        self.last_known = None

    def buffer(self, message):
        self.buffer = []

    def summarize(self):
        self.system_init = summarize
        self.summarized = process()
        return self.summarized.__call__(self.message, self.system_init)

    def record(self):
        summarized = self.summarize()

        with open('core/data/context.json', 'w') as f:
            json.dump(self.message, f)
            if self.logging:
                print("Context recorded.")

        with open('core/memory/full.json', 'w') as f:
            json.dump(self.message, f)
            if self.logging:
                print("Memory recorded.")

        with open('core/memory/summarized.json', 'w') as f:
            json.dump(summarized, f)
            if self.logging:
                print("Context recorded.")
            
