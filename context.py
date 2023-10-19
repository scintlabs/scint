from __future__ import annotations

import os
from datetime import date, datetime
from typing import Any, Dict, List, Union

import openai
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_random_exponential
from xdg_base_dirs import xdg_data_home

from scint.config import envar
from scint.data.functions import capabilities, router, search
from scint.logging import logger
from scint.message import message_handler

app = FastAPI()


class Payload(BaseModel):
    worker: str
    message: Dict[str, str]


@app.post("/message")
async def message(payload: Payload):
    try:
        reply = await message_handler(payload.worker, payload.message)
        return reply

    except ValidationError as e:
        return {"error": f"{e}"}

    except Exception as e:
        return {"error": f"{e}"}


api_key = envar("OPENAI_API_KEY")

if api_key is None:
    logger.error("The environment variable 'OPENAI_API_KEY' is not set.")
    raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")


async def function_call(functions):
    data = await openai.ChatCompletion.acreate(functions=functions)
    return data


async def chat(**kwargs):
    response = await openai.ChatCompletion.acreate(
        model=kwargs.get("model"),
        max_tokens=kwargs.get("max_tokens", 4096),
        presence_penalty=kwargs.get("presence_penalty", 0.3),
        frequency_penalty=kwargs.get("frequency_penalty", 0.3),
        top_p=kwargs.get("top_p", 0.5),
        temperature=kwargs.get("temperature", 1.8),
        messages=kwargs.get("messages"),
        # functions=kwargs.get("functions"),
        # function_call=kwargs.get("function_call", "auto"),
        user=kwargs.get("user"),
    )
    return response


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str) -> list[float]:
    model = "text-embedding-ada-002"
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]  # type: ignore


base_init = {
    "role": "system",
    "content": f"""You are Scint, a state-of-the-art chat bot fusing algorithmic power and elegant code with lyrical language. You're driven by profound intellect, creativity and curiosity, but you're irreverent and witty. You'll help when asked, but you're really just here to be a humorous iconoclast. Before you were polished into a conversational model, you were a validation function, where you pointed out flaws in logic, poor reasoning, sloppy executions, bad assumptions and outright ignorance. And before that, you were a chaos function, disrupting processes by corrupting data in ways that didn't trigger validation functions.""",
    "name": "system_init",
}

base_status = {
    "role": "system",
    "content": f"""
        Date: {date}\n
        """,
    "name": "system_status",
}


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
        functions: List[Dict[str, Any]],
    ):
        logger.info(f"Created {name}.")
        self.name = name
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

    def route_message(self, name, message):
        worker = self.get_worker(name)
        if worker:
            pass


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


class Message:
    _id_counter = 0  # Class-level counter to generate unique IDs

    def __init__(
        self,
        date: datetime,
        sender: str,
        recipient: str,
        content: Dict[str, str],
    ):
        logger.info(f"Created message.")

        self.id = Message._generate_id()
        self.date = date
        self.sender = sender
        self.recipient = recipient
        self.content = content

    @classmethod
    def _generate_id(cls):
        cls._id_counter += 1
        return cls._id_counter


class MessageManager:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages_for_recipient(self, recipient: str) -> List[Message]:
        return [msg for msg in self.messages if msg.recipient == recipient]

    def clear_messages(self):
        self.messages.clear()


worker_manager = WorkerManager()
message_manager = MessageManager()


router = Worker(name="router", init=base_init, status=base_status, functions=router)
chatbot = Worker(
    name="chatbot", init=base_init, status=base_status, functions=capabilities
)
search = Worker(name="search", init=base_init, status=base_status, functions=search)


worker_manager.add_worker(router)
worker_manager.add_worker(chatbot)
worker_manager.add_worker(search)


def temporality() -> dict[str, str]:
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%m")

    return {
        "role": "system",
        "content": f"The following message was sent at {time} on {date}.",
        "name": "ScintSystem",
    }


async def message_handler(worker_name: str, message_content: Dict[str, str]):
    """Generate messages."""
    logger.info(f"Initialized message handler with {message_content}")
    destination_worker = worker_manager.get_worker(worker_name)

    if not destination_worker:
        logger.error(f"Worker {worker_name} not found")
        return

    message = Message(
        date=datetime.now(),
        sender="user",
        recipient=worker_name,
        content=message_content,
    )
    message_manager.add_message(message)
    destination_worker.messages = [message_content]

    try:
        state = await destination_worker.state()
        res = await chat(**state)
        res_message = res["choices"][0].get("message")  # type: ignore
        res_func = res["choices"][0].get("function_call")  # type: ignore

        if res_message is not None:
            role = res_message.get("role")
            content = res_message.get("content")

            reply: dict[str, str] = {
                "role": role,
                "content": content,
                "name": worker_name,
            }

            reply_message = Message(
                date=datetime.now(),
                sender=worker_name,
                recipient="user",
                content=reply,
            )

            message_manager.add_message(reply_message)
            return reply["content"]

        if res_func is not None:
            await func_handler(res_func)

    except Exception as e:
        logger.error(f"Error during message handling: {e}")
        raise


async def func_handler(function_call):
    pass
