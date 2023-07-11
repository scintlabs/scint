from core.providers.openai import api_call
import os
import json

class Context:
    def __init__(self):
        self.current_context = []

    def load_file(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: '{filepath}'")
