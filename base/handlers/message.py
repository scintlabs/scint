import asyncio, enum
from typing import Dict, List

import tenacity

import base.data.db
import base.definitions.prompts
import base.processor
import conf.default
import util.logging
from base.providers.models import openai
from base.definitions.functions import google_search
from base.definitions.classes import MessageRole

prompts = base.definitions.prompts


class MessageHandler:
    def __init__(self):
        util.logging.logger.info(f"Message handler initialized.")

    def format_message(
        self, message: str, role: MessageRole, name: str
    ) -> Dict[str, str]:
        if role not in MessageRole:
            raise ValueError(
                f"Invalid role: {role}. Expected one of {list(MessageRole)}"
            )

        formatted_message = {
            "content": message,
            "role": role.value,
            "name": name,
        }

        return formatted_message

    async def env_data(self):
        dirs = await base.processor.parse_dir()
        files = await base.processor.parse_files()
        data = str(dirs) + str(files)
        env_message = self.format_message(
            data, MessageRole.ASSISTANT, "Environment Data"
        )

        return env_message

    async def build_manifest(self):
        util.logging.logger.info(f"Building message manifest.")

        messages: List[Dict[str, str]] = []
        functions: List[Dict[str, str]] = []

        sys_init = self.format_message(
            prompts.SYSTEM_MESSAGES["controller"], MessageRole.SYSTEM, "Scint"
        )

        messages.append(sys_init)
        functions.append(google_search)

        return messages, functions

    def store_message(self, role, content, response_id):
        try:
            base.data.db.insert_message(role, content, response_id)
            util.logging.logger.info(f"Stored {role} message in the database.")
        except Exception as e:
            util.logging.logger.exception(f"Failed to store message: {e}")


@tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(1))
async def chat(user_message):
    util.logging.logger.info(f"Starting chat process.")

    handler = MessageHandler()

    try:
        messages, functions = await handler.build_manifest()
        formatted_user_message = handler.format_message(
            user_message, MessageRole.USER, conf.default.user
        )
        messages.append(formatted_user_message)

        handler.store_message("user", user_message, None)

        response = await openai(messages, functions)
        data = response["choices"][0]
        reply = None

        try:
            if "content" in data["message"] and data["message"]["content"] is not None:
                reply = data["message"]["content"]
                util.logging.logger.info(f"Response received.\n ❯ {reply}")
                messages.append({"role": "assistant", "content": f"{reply}"})

            if (
                "function_call" in data["message"]
                and data["message"]["function_call"] is not None
            ):
                function_call = data["message"]["function_call"]
                function_results = await base.processor.eval_function(function_call)
                results = await chat(f"{function_results}")
                return results

            if reply:
                handler.store_message("assistant", reply, response["id"])
                return reply

        except Exception as e:
            util.logging.logger.exception(f"There was a problem: {e}")
            raise

    except Exception as e:
        util.logging.logger.exception(
            f"There was a problem delivering the message manifest: {e}"
        )
        raise
