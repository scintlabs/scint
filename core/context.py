from core.providers.openai import api_call
from core.state import State
import os
import json


class Context:
    def __init__(self, name):
        self.name = name
        self.state = State(self.name)

    def events(self):
        self.events = self.state.events

        def prune(self, e):
            self.event = self.events[e]

    def focus():
        if tokenizer(message_buffer) > MAX_TOKENS:
            while tokenizer(message_buffer, gpt4) > MAX_TOKENS / 2.5:
                secondary_message_buffer.append(message_buffer.pop(0))

                with open("secondary_buffer.json", "w") as f:
                    json.dump(secondary_message_buffer, f)
                    manage_buffers()


def rolling_token_count(data):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    prompt_tokens += data["prompt_tokens"]
    completion_tokens += data["completion_tokens"]
    total_tokens += data["total_tokens"]
    return print(f"{prompt_tokens} + {completion_tokens} = {total_tokens}")


def thread_token_count(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens
