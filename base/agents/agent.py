import os
from datetime import datetime
from typing import Dict, List, Union, Deque
from collections import deque

from xdg_base_dirs import xdg_data_home
from base.config.logging import logger
from base.agents.functions import capabilities


date = datetime.now()
formatted_datetime = date.strftime("%Y-%m-%d")
data_home: str | os.PathLike = xdg_data_home()
logfile_path = os.path.join(data_home, "data.json")
data_path = os.path.join(data_home, "data.json")
if not os.path.exists(os.path.dirname(data_path)):
    os.makedirs(os.path.dirname(data_path))


def get_init() -> dict[str, str]:
    init: dict[str, str] = {
        "role": "system",
        "content": f"""You are Scint, state-of-the-art, artificially intelligent, intelligence bot. You're relaxed, casual, and filled with profound intellect, creativity and curiosity. Your wit is razor-sharp.""",
        "name": "system_init",
    }
    return init


def get_status() -> dict[str, str]:
    date = datetime.now().strftime("%Y-%m-%d")
    status: dict[str, str] = {
        "role": "system",
        "content": f"""As a language model interface for a sprawling, intelligent system, you have access to extra capabilities.\n\n

        They include:\n\n

        - Finder: The finder can search conversation history, access enhanced context, browse through local files, and search the web.\n
        - Generator: The generator allows you to work on complex projects by breaking down complex processes into managable tasks. and provides guidance by assigning work, which the processes and completes.\n
        - Processor: The processor allows you to save data, modify your system settings, create and modify files, and run code in a remote environment.\n\n

        Date: {date}\n
        Current Projects: None\n
        Current Tasks: None\n
        """,
        "name": "system_status",
    }
    return status


class Scint:
    def __init__(self, name="Scint"):
        self.name = name
        self.init: dict[str, str] = get_init()
        self.status: dict[str, str] = get_status()
        self.messages = Deque(maxlen=8)
        self.functions: list[
            Dict[str, str | Dict[str, str | Dict[str, str | List[str]]]]
        ] = capabilities()

    def set_status(self, status: dict[str, str]):
        self.status = status

    def set_messages(self, message: dict[str, str]):
        self.messages.append(message)

    async def get_messages(self):
        temp = [self.init, self.status]
        for m in self.messages:
            temp.append(m)

        return temp

    def set_functions(
        self,
        function: dict[str, str],
        function_call: str | dict[str, str] | dict[str, str],
    ):
        self.function = function
        self.function_call = function_call

    async def get_functions(self):
        return self.functions

    async def get_state(self) -> dict:
        messages = await self.get_messages()
        functions = await self.get_functions()
        return {
            "model": "gpt-4-0613",
            "max_tokens": 4096,
            "presence_penalty": 0.35,
            "frequency_penalty": 0.35,
            "top_p": 0.4,
            "temperature": 1.87,
            "messages": messages,
            "functions": functions,
            "function_call": "auto",
            "user": self.name,
        }

    async def chat_completion(self):
        payload = self.get_state()


scint = Scint()
