import os
from datetime import datetime
from typing import Dict, List, Any, Union, Optional

from xdg_base_dirs import xdg_data_home
from scint.services.logging import logger
from scint.workers.functions import capabilities
from scint.workers.prompts import base_init, base_status

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
    def __init__(
        self,
        name: str,
        init: Dict[str, str],
        status: Dict[str, str],
        target: str | None,
        functions: List[Dict[str, Any]] = capabilities,
    ):
        logger.info(f"Created {name}.")
        self.name = name
        self.target = target
        self.init = init
        self.status = status
        self.functions = functions
        self.messages: List[Dict[str, str]] = []
        self.config = {}

    async def state(self) -> Dict[str, Any]:
        config = await set_config()
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


async def get_init(init: Dict[str, str]) -> Dict[str, str]:
    logger.info(f"Init.")
    return init


async def get_status(status: Dict[str, str]) -> Dict[str, str]:
    logger.info(f"Status.")
    return status


async def get_functions(worker_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    return worker_state["functions"]


async def set_config(
    model: str = GPT4,
    max_tokens: int = 4096,
    presence_penalty: float = 0.35,
    frequency_penalty: float = 0.35,
    top_p: float = 0.4,
    temperature: float = 1.87,
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
    worker: Dict[str, Any],
    function: Dict[str, str],
    function_call: Union[str, Dict[str, str]],
) -> Dict[str, Any]:
    worker["function"] = function
    worker["function_call"] = function_call
    return worker


async def set_status(worker: Dict[str, Any], status: Dict[str, str]) -> Dict[str, Any]:
    worker["status"] = status
    return worker


async def set_messages(worker_state, message) -> Dict[str, str]:
    worker_state.messages.append(message)
    return worker_state


async def get_messages(worker_state):
    return worker_state.messages


async def get_config(worker: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "model": worker["model"],
        "max_tokens": worker["max_tokens"],
        "temperature": worker["temperature"],
        "presence_penalty": worker["presence_penalty"],
        "frequency_penalty": worker["frequency_penalty"],
        "top_p": worker["top_p"],
    }
