import asyncio
import json
import os
from typing import Dict, List

from tenacity import retry, stop_after_attempt, wait_fixed

from core.providers.models import openai
from core.definitions.functions import generate_code, google_search
from core.processor import eval_function, parse_dir
from core.state import State
from util.logging import logger

system_message: str = "You are Scint, a stateful, collaborative, intelligent assistant. You have access to a secure sandbox environment which you can use to evaluate Python code. You can also create files and directories in this environment to build more complex projects."


class MessageHandler:
    logger.info(f"Calling message handler.")
    """Message handler class. It handles messages."""

    def __init__(self):
        self.roles = ["system", "assistant", "user"]
        self.message_template = lambda message, role, name: {
            "content": f"{message}",
            "role": f"{role}",
            "name": f"{name}",
        }

    def format_message(self, user_message):
        return self.message_template(user_message, self.roles[2], "Tim")

    async def build_manifest(self):
        logger.info(f"Building message package manifest.")

        messages: List[Dict[str, str]] = []
        functions: List[Dict[str, str]] = []
        # env_data = await parse_env()
        sys_init = self.message_template(system_message, self.roles[0], "system")
        # data = self.message_template("None", str(self.roles[1]), "environment")

        messages.append(sys_init)
        # messages.append(data)
        functions.append(google_search)
        functions.append(generate_code)

        return messages, functions


# @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def chat(user_message):
    logger.info(f"Starting chat process.")

    handler = MessageHandler()

    messages, functions = await handler.build_manifest()  # type: ignore
    formatted_user_message = handler.format_message(user_message)
    messages.append(formatted_user_message)

    try:
        response = await openai(messages, functions)  # type: ignore
        logger.info(f"Sending message manifest.")
        data = response["choices"][0]  # type: ignore
        reply = None

        if "content" in data["message"] and data["message"]["content"] is not None:
            reply = data["message"]["content"]
            logger.info(f"Response received: {reply}")
            messages.append({"role": "assistant", "content": f"{reply}"})  # type: ignore

        if (
            "function_call" in data["message"]
            and data["message"]["function_call"] is not None
        ):
            function_call = data["message"]["function_call"]
            function_results = await eval_function(function_call)
            results = await chat(f"{function_results}")  # type: ignore
            return results

        # Return the reply if it exists
        if reply:
            return reply

    except Exception as e:
        logger.exception(f"There was a problem delivering the message manifest: {e}")
        raise
