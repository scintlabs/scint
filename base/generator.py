from typing import Dict, List

from tenacity import retry, stop_after_attempt, wait_fixed

from base.providers.models import openai
from base.definitions.prompts import Prompt
from util.logging import logger

generate_prose = {
    "name": "generate_code",
    "description": "Use this function to write and test Python code. Files are created in a secure environment.",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to write and execute. You may write files and folders to create complex projects using Python.",
            },
        },
        "required": ["code"],
    },
}

generate_code = {
    "name": "generate_code",
    "description": "Use this function to write and test Python code. Files are created and executed in a secure environment.",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to write and execute. You may write files and folders to create complex projects using Python.",
            },
        },
        "required": ["code"],
    },
}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def generate(message: str, prompts: List[Prompt]) -> List[Dict]:
    """
    Experimental function for mutating data with multiple, functional prompts.
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

            response = await openai(messages, functions)  # type: ignore
            data = response["choices"][0]  # type: ignore
            generated = data["message"].get("content")
            messages.append({"role": "system", "content": f"{generated}."})
            print(f"{generated}")

        print(messages)
        return messages

    except Exception as e:
        logger.exception(f"The generator was halted: {e}")
        raise


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def complete(message: str, prompt: List[Prompt]) -> str:
    """"""
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": message})
    response = await openai(messages, functions)  # type: ignore

    if response is None:
        raise ValueError("Error.")

    message = response["choices"][0]["message"].get("content")  # type: ignore
    return message
