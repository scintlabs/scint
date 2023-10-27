import json
import importlib
from typing import Dict, List, Any

from core.config import GPT4
from services.openai import completion
from services.logger import log
from core.message import Message


class Worker:
    def __init__(self, name, system_init, function):
        log.info(f"Initializing {name}.")
        self.name: str = name
        self.system_init: Dict[str, str] = system_init
        self.messages: List[Dict[str, str]] = [self.system_init]
        self.function: Dict[str, Any] = function
        self.function_call: Dict[str, str] = {"name": function.get("name")}
        self.config: Dict[str, Any] = {}

    async def state(self) -> Dict[str, Any]:
        log.info(f"Getting current state for {self.name}.")
        config = await self.set_config()
        messages = []

        for m in self.messages:
            messages.append(m)

        state = {
            "messages": messages,
            "functions": [self.function],
            "function_call": self.function_call,
            "model": config.get("model"),
            "max_tokens": config.get("max_tokens"),
            "presence_penalty": config.get("presence_penalty"),
            "frequency_penalty": config.get("frequency_penalty"),
            "top_p": config.get("top_p"),
            "temperature": config.get("temperature"),
        }

        return state

    async def process_request(self, payload):
        log.info(f"Processing request.")
        self.payload: Message = payload
        self.messages.append(payload.message)
        state = await self.state()
        res = await completion(**state)
        res_message = res["choices"][0].get("message")  # type: ignore

        if not isinstance(res_message, dict):
            log.error("res_message is not a dictionary.")
            return

        function_call = res_message.get("function_call")

        if function_call is not None:
            return await self.eval_function_call(res_message)  # type: ignore

    async def generate_reply(self, res_message):
        log.info("Generating reply.")

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
        log.info("Evaluating worker function call.")

        function_call = res_message.get("function_call")
        function_name = function_call.get("name")
        function_args = function_call.get("arguments")

        if isinstance(function_args, str):
            function_args = json.loads(function_args)

        if function_name.strip() == self.function.get("name"):
            module_name = "handlers.weather"
            module = importlib.import_module(module_name)
            method_to_call = getattr(module, function_name, None)

            if method_to_call:
                try:
                    result = await method_to_call(**function_args)
                    result_message = Message(self.name, "Interface", result)
                    return result_message

                except Exception as e:
                    log.error(f"Error during function call: {e}")
            else:
                log.error(f"Function {function_name} not found in {module_name}.")
        else:
            log.error(
                f"Function name mismatch. Expected: {self.function.get('name')}, Received: {function_name}"
            )

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
