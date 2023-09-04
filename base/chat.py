import asyncio
from typing import Dict, List

from tenacity import retry, stop_after_attempt, wait_fixed

import base.handlers.db_connection
import base.definitions.prompts
import base.processor
import conf.app
from base.handlers.message import MessageHandler
from base.providers.openai import openai
from base.definitions.classes import MessageRole
from util.logging import logger


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def chat(user_message):
    logger.info(f"Starting chat process.")

    handler = MessageHandler()

    try:
        messages, functions = await handler.build_manifest()
        formatted_user_message = handler.format_message(
            user_message, MessageRole.USER, conf.app.user
        )
        messages.append(formatted_user_message)

        handler.store_message("user", user_message, None)

        response = await openai(messages, functions)
        data = response["choices"][0]
        reply = None

        try:
            if "content" in data["message"] and data["message"]["content"] is not None:
                reply = data["message"]["content"]
                logger.info(f"Response received.\n ❯ {reply}")
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
            logger.exception(f"There was a problem: {e}")
            raise

    except Exception as e:
        logger.exception(f"There was a problem delivering the message manifest: {e}")
        raise
