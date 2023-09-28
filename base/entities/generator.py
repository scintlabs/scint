from typing import Dict, List

from base.agents import Agent
from processing import Prompt
from providers.openai import chat_completion
from base.observability.logging import logger

from config.functions import Generator as Generator_funcs
from config.prompts import Generator as Generator_prompt


async def transform_data(message: str, prompts: List[Prompt]) -> List[Dict]:
    """
    This function loops multiple promps over an input, modifying it and passing the results cumulitively along the pipeline.
    """
    messages = []
    messages.append({"role": "system", "content": message})

    try:
        for prompt in prompts:
            prompt_content = prompt

            if len(messages) == 1:
                messages.insert(0, {"role": "system", "content": prompt_content})
            else:
                messages[0] = {"role": "system", "content": prompt_content}

            response = await chat(messages, functions)  # type: ignore
            data = response["choices"][0]  # type: ignore
            generated = data["message"].get("content")
            messages.append({"role": "system", "content": f"{generated}."})
            print(f"{generated}")

        return messages

    except Exception as e:
        logger.exception(f"The generator was halted: {e}")
        raise


async def complete(message: str, prompt: List[Prompt]) -> str:
    """"""
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": message})
    response = await chat(messages, functions)  # type: ignore

    if response is None:
        raise ValueError("Error.")

    message = response["choices"][0]["message"].get("content")  # type: ignore
    return message
