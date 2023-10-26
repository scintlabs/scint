import os
import json
from datetime import datetime
from typing import Dict, List, Any, Union

from xdg_base_dirs import xdg_data_home

from services.config import GPT4
from services.openai import completion
from services.logger import log
from workers.weather import get_weather
from core.message import Message


date = datetime.now()
formatted_datetime = date.strftime("%Y-%m-%d")
data_home: str | os.PathLike = xdg_data_home()
logfile_path = os.path.join(data_home, "data.json")
data_path = os.path.join(data_home, "data.json")
if not os.path.exists(os.path.dirname(data_path)):
    os.makedirs(os.path.dirname(data_path))


class RefactoredWorker:
    def __init__(
        self, name: str, init: Dict[str, str], functions: List[Dict[str, Any]]
    ):
        log.info(f"Initialized {name}.")

        self.name = name
        self.system_init = init
        self.messages = [init]
        self.functions = functions
        self.config = self.default_config()

    def default_config(self) -> Dict[str, Any]:
        return {
            "model": GPT4,
            "max_tokens": 1024,
            "presence_penalty": 0.3,
            "frequency_penalty": 0.3,
            "top_p": 0.9,
            "temperature": 1.9,
        }

    async def state(self) -> Dict[str, Any]:
        log.info(f"Getting current state for {self.name}.")
        config = await self.set_config()
        state = {
            "user": self.name,
            "messages": self.messages,
            "functions": self.functions,
            **config,
        }
        log.info(f"{state}.")
        return state

    async def process_request(
        self, payload: Dict[str, Any]
    ) -> Union[Dict[str, Any], None]:
        if not payload:
            log.error("Received None payload.")
            return

        log.info(f"Processing request: {payload}")

        self.messages.append(payload.get("message", {}))
        state = await self.state()
        res = await self.chat(state)
        res_message = res.get("choices", [{}])[0].get("message")

        if not isinstance(res_message, dict):
            log.error("res_message is not a dictionary.")
            return

        content = res_message.get("content")
        function_call = res_message.get("function_call")

        if content:
            return await self.generate_reply(res_message)
        elif function_call:
            return await self.handle_function_call(res_message)

    async def chat(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for the chat logic.
        # In the original code, there's a call to chat with the state.
        # This is just a stub to simulate that behavior.
        return {
            "choices": [
                {"message": {"content": "sample content", "function_call": None}}
            ]
        }

    async def generate_reply(self, res_message: Dict[str, Any]) -> Dict[str, Any]:
        log.info("Generating response.")
        role = res_message.get("role")
        content = res_message.get("content")

        if not (role and content):
            log.error("Role or content missing in res_message.")
            return {}

        return {
            "sender": self.name,
            "recipient": "user",
            "message": {"role": role, "content": content, "name": self.name},
        }

    async def handle_function_call(
        self, res_message: Dict[str, Any]
    ) -> Union[Dict[str, Any], None]:
        log.info("Evaluating function call.")
        function_call = res_message.get("function_call", {})
        function_name = function_call.get("name")
        function_args = json.loads(function_call.get("arguments", "{}"))

        if not (function_name and function_args):
            log.error("Function name or arguments missing.")
            return

        if function_name == "get_weather":
            return await self.get_weather(function_args)

    async def get_weather(
        self, function_args: Dict[str, Any]
    ) -> Union[Dict[str, Any], None]:
        city = function_args.get("city")
        if not city:
            log.error("City argument missing for get_weather function.")
            return

        try:
            log.info(f"Fetching weather for city: {city}")
            # Placeholder for fetching weather.
            # In the original code, there's a call to fetch the weather.
            # This is just a stub to simulate that behavior.
            return {"weather": "sunny", "temperature": 25}
        except Exception as e:
            log.error(f"Error while fetching weather: {e}")

    # Rest of the methods remain unchanged for now, as they're mostly getters and setters.

    async def get_init(self, init: Dict[str, str]) -> Dict[str, str]:
        return init

    async def get_status(self, status: Dict[str, str]) -> Dict[str, str]:
        return status

    async def get_functions(self, worker_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        return worker_state["functions"]

    async def set_config(
        self,
        model: str = "GPT4",
        max_tokens: int = 1024,
        presence_penalty: float = 0.3,
        frequency_penalty: float = 0.3,
        top_p: float = 0.9,
        temperature: float = 1.9,
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


class Worker:
    def __init__(self, name, system_init, function):
        log.info(f"Initialized {name}.")
        self.name: str = name
        self.system_init: Dict[str, str] = system_init
        self.function: List[Dict[str, Any]] = function
        self.messages: List[Dict[str, str]] = [self.system_init]
        self.config: Dict[str, Any] = {}

    async def state(self) -> Dict[str, Any]:
        log.info(f"Getting current state for {self.name}.")
        config = await self.set_config()
        messages = []

        for m in self.messages:
            messages.append(m)

        state = {
            "messages": messages,
            "functions": self.function,
            "model": config.get("model"),
            "max_tokens": config.get("max_tokens"),
            "presence_penalty": config.get("presence_penalty"),
            "frequency_penalty": config.get("frequency_penalty"),
            "top_p": config.get("top_p"),
            "temperature": config.get("temperature"),
        }

        return state

    async def process_request(self, payload):
        log.info(f"Processing request: {payload}")
        self.payload: Message = payload
        self.messages.append(payload.message)
        state = await self.state()
        res = await completion(**state)
        res_message = res["choices"][0].get("message")  # type: ignore

        if not isinstance(res_message, dict):
            log.error("res_message is not a dictionary.")
            return

        content = res_message.get("content")
        function_call = res_message.get("function_call")

        if content is not None:
            reply = await self.generate_reply(res_message)
            return reply

        elif function_call is not None:
            new_request = await self.eval_function_call(res_message)  # type: ignore

            if new_request:
                return await self.process_request(new_request)

            else:
                log.error("Function call did not return a valid request.")
                return

    async def generate_reply(self, res_message):
        log.info("Generating response.")

        role = res_message.get("role")
        content = res_message.get("content")

        if not role or not content:
            log.error("Role or content missing in res_message.")
            return

        reply_message: dict[str, str] = {
            "role": role,
            "content": content,
            "name": self.name,
        }

        reply = Message(
            sender=self.name,
            recipient="user",
            message=reply_message,
        )

        return reply

    async def eval_function_call(self, res_message):
        log.info("Evaluating function call.")

        function_call = res_message.get("function_call")
        function_name = function_call.get("name")
        function_args = function_call.get("arguments")
        function_args = json.loads(function_args)

        if not function_name or not function_args:
            log.error("Function name or arguments missing.")
            return

        if function_name.strip() == "get_weather":
            log.info("Proceeding to fetch weather...")

            city = function_args.get("city")

            if not city:
                log.error("City argument missing for get_weather function.")
                return

            try:
                log.info(f"Fetching weather for city: {city}")
                response = await get_weather(city)
                return response

            except Exception as e:
                log.error(f"Error while fetching weather: {e}")
        else:
            log.error("Function name is not 'get_weather'.")

    async def get_init(self, init: Dict[str, str]) -> Dict[str, str]:
        log.info(f"Init.")
        return init

    async def get_status(self, status: Dict[str, str]) -> Dict[str, str]:
        log.info(f"Status.")
        return status

    async def get_functions(self, worker_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        return worker_state["functions"]

    async def set_config(
        self,
        model: str = GPT4,
        max_tokens: int = 1024,
        presence_penalty: float = 0.3,
        frequency_penalty: float = 0.3,
        top_p: float = 0.9,
        temperature: float = 1.9,
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
