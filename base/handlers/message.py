from datetime import datetime

from base.system.logging import logger
from base.agent.agent import scint
from base.system.providers.openai import chat


def temporality() -> dict[str, str]:
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%m")

    return {
        "role": "system",
        "content": f"The following message was sent at {time} on {date}.",
        "name": "ScintSystem",
    }


async def message_handler(message):
    """Handle messages to and from models."""
    logger.info(f"Initialized message handler with {scint.messages}")
    await scint.set_messages(temporality())
    await scint.set_messages(message)

    try:
        state: dict = await scint.get_state()
        response = await chat(**state)
        response_message = response["choices"][0].get("message")  # type: ignore
        function_call = response["choices"][0].get("message")  # type: ignore

        if response_message is not None:
            role = response_message.get("role")
            content = response_message.get("content")
            reply = {"role": role, "content": content, "name": "Scint"}
            await scint.set_messages(reply)
            return reply["content"]

        if function_call is not None:
            await function_handler(function_call)

    except Exception as e:
        logger.error(f"Error during message handling: {e}")
        raise


async def function_handler(function_call):
    """Hundle function calls from models."""
    logger.info(f"```{function_call}```")
