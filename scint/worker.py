import os
from datetime import datetime
from typing import Any, Dict, List, Union

from xdg_base_dirs import xdg_data_home

from scint.logging import logger

date = datetime.now()
formatted_datetime = date.strftime("%Y-%m-%d")
data_home: str | os.PathLike = xdg_data_home()
logfile_path = os.path.join(data_home, "data.json")
data_path = os.path.join(data_home, "data.json")
if not os.path.exists(os.path.dirname(data_path)):
    os.makedirs(os.path.dirname(data_path))


GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4-0613"


class Worker:
    def __init__(self, name, init, status, functions):
        logger.info(f"Worker initialized: {name}.")

        self.name: str = name
        self.init: Dict[str, str] = init
        self.status: Dict[str, str] = status
        self.functions: List[Dict[str, Any]] = functions
        self.messages: List[Dict[str, str]] = []
        self.config: Dict[str, Any] = {}

    async def state(self) -> Dict[str, Any]:
        config = await self.set_config()
        messages = []
        messages.append(self.init)
        messages.append(self.status)

        for m in self.messages:
            messages.append(m)

        return {
            "user": self.name,
            "messages": messages,
            "functions": self.functions,
            "model": config.get("model"),
            "max_tokens": config.get("max_tokens"),
            "presence_penalty": config.get("presence_penalty"),
            "frequency_penalty": config.get("frequency_penalty"),
            "top_p": config.get("top_p"),
            "temperature": config.get("temperature"),
        }

    async def get_init(self, init: Dict[str, str]) -> Dict[str, str]:
        logger.info(f"Init.")
        return init

    async def get_status(self, status: Dict[str, str]) -> Dict[str, str]:
        logger.info(f"Status.")
        return status

    async def get_functions(self, worker_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        return worker_state["functions"]

    async def set_config(
        self,
        model: str = GPT4,
        max_tokens: int = 1024,
        presence_penalty: float = 0.45,
        frequency_penalty: float = 0.45,
        top_p: float = 0.5,
        temperature: float = 1.95,
    ) -> Dict[str, Any]:
        return {
            "model": model,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "top_p": top_p,
            "temperature": temperature,
        }

    async def set_functions(
        self,
        worker: Dict[str, Any],
        function: Dict[str, str],
        function_call: Union[str, Dict[str, str]],
    ) -> Dict[str, Any]:
        worker["function"] = function
        worker["function_call"] = function_call
        return worker

    async def set_status(
        self, worker: Dict[str, Any], status: Dict[str, str]
    ) -> Dict[str, Any]:
        worker["status"] = status
        return worker

    async def set_messages(self, worker_state, message) -> Dict[str, str]:
        worker_state.messages.append(message)
        return worker_state

    async def get_messages(self, worker_state):
        return worker_state.messages

    async def get_config(self, worker: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "model": worker["model"],
            "max_tokens": worker["max_tokens"],
            "temperature": worker["temperature"],
            "presence_penalty": worker["presence_penalty"],
            "frequency_penalty": worker["frequency_penalty"],
            "top_p": worker["top_p"],
        }


class WorkerManager:
    def __init__(self):
        self.workers = {}

    def add_worker(self, worker):
        self.workers[worker.name] = worker

    def remove_worker(self, name):
        if name in self.workers:
            del self.workers[name]

    def get_worker(self, name):
        return self.workers.get(name, None)
