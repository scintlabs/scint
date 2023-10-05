import json
from datetime import datetime

from base.config.logging import logger
from base.agents.agent import scint
from base.providers.openai import chat, chat_completion, function_call


async def message_handler(message):
    """Hundle message processing and formatting"""
    logger.info(f"Initialized message handler with {scint.messages}")

    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%m")
    temporality = {
        "role": "system",
        "content": f"The following message was set at {time} on {date}.",
        "name": "ScintSystem",
    }
    scint.set_messages(temporality)
    scint.set_messages(message)

    try:
        state: dict = await scint.get_state()
        response = await chat(**state)
        response_message = response["choices"][0].get("message")  # type: ignore
        function_call = response["choices"][0].get("message")  # type: ignore

        if response_message is not None:
            role = response_message.get("role")
            content = response_message.get("content")
            reply = {"role": role, "content": content, "name": "Scint"}
            scint.set_messages(reply)
            return reply["content"]

        if function_call is not None:
            await function_handler(function_call)

    except Exception as e:
        logger.error(f"{e}")


async def function_handler(function_call):
    """Hundle function calls from models."""
    logger.info(f"```{function_call}```")
