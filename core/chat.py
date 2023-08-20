import os, asyncio
from typing import Any, Tuple, List, Dict
from core.state import State
from core.processor import parse_env, parse_files, eval_function
from core.data.providers import openai_chat
from core.definitions.functions import generate_code as functions
from tenacity import retry, stop_after_attempt, wait_fixed
from util.logger import logger

state = State()

system_message: str = "You are Scint, a stateful, collaborative, intelligent assistant. You have access to a secure sandbox environment which you can use to evaluate Python code. You can also create files and directories in this environment to build more complex projects."


class MessageHandler:
    def __init__(self):
        self.messages: List[Dict[str, str]]
        self.roles = ["system", "assistant", "user"]
        self.message_template = lambda message, role, name: {
            "role": f"{role}",
            "content": f"{message}",
            "name": f"{name}",
        }

    def format_message(self, user_message):
        return self.message_template(user_message, self.roles[2], "Tim")

    async def get_data(self):
        self.env_data = await parse_env()
        return self.env_data

    async def build_manifest(self):
        system_init = self.message_template(system_message, self.roles[0], "directive")
        data = self.message_template(
            await self.get_data(), self.roles[1], "environment"
        )

        return system_init, data


handler = MessageHandler()


# @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def chat(user_message):
    message = handler.format_message(user_message)
    manifest = await handler.build_manifest()  # type: ignore
    messages = list(manifest)
    messages.append(message)  # type: ignore

    try:
        response = await openai_chat(messages, functions)  # type: ignore
        data = response["choices"][0]
        reply = data["message"].get("content")

        messages.append({"role": "assistant", "content": f"{reply}"})  # type: ignore

        if data["message"]["function_call"] is not None:
            function_call = data["message"]["function_call"]
            await eval_function(function_call)

        return reply

    except Exception as e:
        raise
