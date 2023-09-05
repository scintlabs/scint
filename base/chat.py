import asyncio
from typing import Dict, List

from tenacity import retry, stop_after_attempt, wait_fixed

import base.definitions.prompts
import base.providers.openai as openai
import base.processor
from base.definitions.types import Message
from base.handlers.message import MessageHandler
from util.logging import logger


# @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def send_message(message: Message):
    logger.info(f"Sending message: {message.content}")
    handler = MessageHandler()

    try:
        logger.info(f"Sending message payload.")
        messages, functions = await handler.build_manifest(message)
        response = await openai.chat(messages, functions)

        if isinstance(response, tuple) and len(response) == 2:
            response_message, response_function = response
        else:
            response_message = response
            response_function = None

        logger.info(
            f"Response from {response_message.author.name}.\n ❯ {response_message.content}"
        )

    except Exception as e:
        logger.exception(f"There was a problem delivering the message: {e}")
        raise
