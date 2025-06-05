from __future__ import annotations

from enum import Enum

from src.runtime.utils import timestamp


class Event(Enum):
    FunctionCall = {"type": "function_call"}
    FunctionCallOutput = {"type": "function_call_output"}


class ExecutionEvent(Enum):
    Execution = {"type": "function_call"}
    Result = {"type": "function_call_output"}


class ThreadEvent(Enum):
    Created = {"created": lambda: timestamp()}
    Staled = {"staled": lambda: timestamp()}
    Encoded = {"encoded": lambda: timestamp()}
    Pruned = {"purged": lambda: timestamp()}

    def __init__(self, event):
        self.event = event

    def __call__(self, content: str = None):
        if content is not None:
            self.event["content"] = content
        return self.event
