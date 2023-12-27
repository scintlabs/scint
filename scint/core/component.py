from datetime import datetime
from typing import Any, Dict

from scint.core.messages import Message
from scint.services.logger import log


class SystemStatus:
    def __init__(self):
        self.date: datetime = datetime.now().strftime("%Y-%m-%d")
        self.time: datetime = datetime.now().strftime("%H:%M")
        self.projects: Dict[str, str] = {}
        self.tasks: Dict[str, str] = {}
        self.events: Dict[str, str] = {}

    def get(self) -> str:
        return {
            f"""It's currently {self.time} on {self.date}. Current projects include {self.projects}. Current tasks include {self.tasks}. Upcoming events include {self.events}."""
        }


class Component:
    def __init__(self):
        self.name = None
        self.identity = None
        self.instructions = None
        self.config = None
        self.system_status = SystemStatus()

    def get_state(self) -> Dict[str, Any]:
        messages = []
        init = f"{self.identity}\n\n{self.instructions}\n\n{self.system_status.get()}"
        init_message = Message("system", init, self.name)
        messages.append(init_message.data_dump())

        state = {
            "model": self.config.get("model"),
            "temperature": self.config.get("temperature"),
            "top_p": self.config.get("top_p"),
            "max_tokens": self.config.get("max_tokens"),
            "presence_penalty": self.config.get("presence_penalty"),
            "frequency_penalty": self.config.get("frequency_penalty"),
            "messages": messages,
        }

        if self.tools is not None:
            state["tools"] = self.tools.data_dump()

        log.info(f"{self.name}: got state.")
        return state
