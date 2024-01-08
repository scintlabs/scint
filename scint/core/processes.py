import json
from datetime import datetime
from typing import Dict, List, Any

from scint.conf import CONF
from scint.core.context import Context
from scint.core.messages import SystemMessage, UserMessage
from scint.core.tools import Tools
from scint.services.openai import tool_completion
from scint.services.logger import log


class SystemStatus:
    def __init__(self):
        self.date: datetime = datetime.now().strftime("%Y-%m-%d")
        self.time: datetime = datetime.now().strftime("%H:%M")
        self.projects: Dict[str, str] = {}
        self.tasks: Dict[str, str] = {}
        self.events: Dict[str, str] = {}

    def get(self) -> str:
        return f"""It's currently {self.time} on {self.date}. Current projects include {self.projects}. Current tasks include {self.tasks}. Upcoming events include {self.events}."""


class ProcessMeta(type):
    def __new__(cls, name, bases, dct):
        dct["metadata"] = cls.create_default_metadata(dct)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def create_default_metadata(dct):
        return {
            "model": dct.get("model"),
            "temperature": dct.get("temperature"),
            "top_p": dct.get("top_p"),
            "max_tokens": dct.get("max_tokens"),
            "presence_penalty": dct.get("presence_penalty"),
            "frequency_penalty": dct.get("frequency_penalty"),
            "tool_choice": dct.get("auto"),
        }

    @classmethod
    def get_tools(self):
        tools = {}

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "tool_metadata"):
                tools[attr_name] = attr.tool_metadata

        return tools

    @classmethod
    def set_tools(cls, tools: Tools):
        cls.tools = tools


class Process(metaclass=ProcessMeta):
    def __init__(self, identity=None, instructions=None, config=None, tools=None):
        self.metadata = self.__class__.create_default_metadata(self.__class__.__dict__)
        self.name = self.__class__.__name__
        self.identity = identity
        self.instructions = instructions
        self.config = config if config is not None else CONF
        self.tools = tools if tools is not None else Tools()
        self.system_status = SystemStatus()
        self.context = Context()

    def get_state(self) -> Dict[List, Any]:
        messages = []
        init = f"{self.identity}\n\n{self.instructions}\n\n{self.system_status.get()}"
        init_message = SystemMessage(init, self.__class__.__name__)
        messages.append(init_message.data_dump())

        for message in self.context.messages:
            messages.append(message.data_dump())

        return {
            "model": self.config.get("model"),
            "temperature": self.config.get("temperature"),
            "top_p": self.config.get("top_p"),
            "max_tokens": self.config.get("max_tokens"),
            "presence_penalty": self.config.get("presence_penalty"),
            "frequency_penalty": self.config.get("frequency_penalty"),
            "messages": messages,
            "tools": self.tools.data_dump(),
            "tool_choice": "auto",
        }

    async def call(self, message: UserMessage):
        self.context.add(message)
        state = self.get_state()
        log.info(state)

        try:
            async for completions in tool_completion(**state):
                for tool_call in completions:
                    function = tool_call.get("function")
                    tool_name = function.get("name")
                    func_args = json.loads(function.get("arguments", "{}"))
                    tool_instance = self.tools.get(tool_name)

                    try:
                        if tool_instance is not None:
                            response = await tool_instance.execute_action(**func_args)
                            log.info(response.data_dump())
                            yield response

                    except Exception as e:
                        log.error(f"{self.__class__.__name__}: {e}")
                        raise

        except Exception as e:
            log.error(f"{self.__class__.__name__}: {e}")
            raise


class Processes:
    def __init__(self, processes: Dict[str, Process] = {}):
        self._processes = processes

    def __iter__(self):
        return iter(self._processes.values())

    def add(self, process: Process):
        self._processes[process.name] = process

    def remove(self, process_name):
        if process_name in self._processes:
            del self._processes[process_name]
