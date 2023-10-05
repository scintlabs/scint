import os
from datetime import datetime
from typing import Dict, List, Coroutine, Any, Deque
from enum import Enum

from xdg_base_dirs import xdg_data_home
from base.system.logging import logger
from base.agent.functions import capabilities


date = datetime.now()
formatted_datetime = date.strftime("%Y-%m-%d")
data_home: str | os.PathLike = xdg_data_home()
logfile_path = os.path.join(data_home, "data.json")
data_path = os.path.join(data_home, "data.json")
if not os.path.exists(os.path.dirname(data_path)):
    os.makedirs(os.path.dirname(data_path))


GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4-0613"


def get_init() -> dict[str, str]:
    logger.info(f"Created initialization prompt.")
    init = {
        "role": "system",
        "content": f"""You are Scint, state-of-the-art, artificially intelligent, intelligence bot. You're relaxed, casual, and filled with profound intellect, creativity and curiosity. Your wit is razor-sharp.""",
        "name": "system_init",
    }
    return init


def get_status() -> dict[str, str]:
    logger.info(f"Created status prompt.")
    date = datetime.now().strftime("%Y-%m-%d")
    status = {
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
    def __init__(self, name):
        logger.info(f"Created {name}.")

        self.name = name
        self.config = self.set_config()
        self.init = get_init()
        self.status = get_status()
        self.messages = []
        self.functions: list[
            Dict[str, str | Dict[str, str | Dict[str, str | List[str]]]]
        ] = capabilities()

    def set_status(self, status: dict[str, str]):
        self.status = status

    async def set_messages(self, message: dict[str, str]):
        self.messages.append(message)

    async def get_messages(self):
        init = self.init
        status = self.status
        temp = [init, status]

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

    def set_config(
        self,
        model: str = GPT4,
        max_tokens: int = 4096,
        presence_penalty: float = 0.35,
        frequency_penalty: float = 0.35,
        top_p: float = 0.4,
        temperature: float = 1.87,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.top_p = top_p

    async def get_config(self):
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "top_p": self.top_p,
        }

    async def get_state(self) -> dict:
        messages = await self.get_messages()
        functions = await self.get_functions()
        config = await self.get_config()

        return {
            "user": self.name,
            "messages": messages,
            "functions": functions,
            "function_call": "auto",
            "model": config["model"],
            "max_tokens": config["max_tokens"],
            "presence_penalty": config["presence_penalty"],
            "frequency_penalty": config["frequency_penalty"],
            "top_p": config["top_p"],
            "temperature": config["temperature"],
        }


scint = Scint(name="Scint")
