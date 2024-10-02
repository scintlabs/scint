from typing import Any, Dict, Optional

from scint.framework.types.model import Model


class Event(Model):
    name: str
    data: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_occurence()

    def on_occurence(self):
        return print(self.data)


class MethodCall(Event):
    arguments: Dict[str, Any] = {}


class CallResult(Event):
    result: Optional[str] = None
